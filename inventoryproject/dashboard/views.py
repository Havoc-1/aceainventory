import datetime
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Delivery, Location, Inventory, DeliveryItem, Quotation, QuotationItem, Type
from .forms import CategoryForm, DeliveryForm, InventoryForm, DeliveryItemForm, DeliveryItemFormSet, QuotationForm, QuotationItemForm, QuotationItemFormSet
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user.models import UserProfile
from django.forms import inlineformset_factory

# P.S. path has to be reflected also in urls.py
@login_required
def index(request):
    if 'searchBar' in request.GET:                          # Search Functionality
        searchBar = request.GET['searchBar']
        multiple_query = Q(Q(name__icontains=searchBar) | Q(location__icontains=searchBar))
        inventory = Inventory.objects.filter(multiple_query)
    else: 
        inventory = Inventory.objects.all                    # makes it so inventory can be viewed by non-staff (ENGINEERING)                
    context ={
        'inventory': inventory,
    }
    return render(request, 'dashboard/index.html', context)

class inventoryView(LoginRequiredMixin, View):
    template_name = 'dashboard/inventory.html'
    def get_context_data(self, **kwargs):
        inventory = Inventory.objects.all
        kwargs['inventory'] = inventory
        filteredInventory = inventory = Inventory.objects.filter(location=self.request.user.userprofile.location)
        kwargs['filteredInventory'] = filteredInventory
        if 'inventory_form' not in kwargs:
            kwargs['inventory_form'] = InventoryForm()
        if 'category_form' not in kwargs:
            kwargs['category_form'] = CategoryForm()

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}
        print(request.POST)
        if 'inventory' in request.POST:
            inventory_form = InventoryForm(request.POST)

            if inventory_form.is_valid():
                inventory_form.clean()
                prod = inventory_form.clean()
                print(prod)
                print(prod.get('location'))
                if request.method == 'POST':

                    print(request.POST.get('location'))
                    form_data = {'name': inventory_form.cleaned_data['name'],
                                'type': inventory_form.cleaned_data['type'],
                                'location': inventory_form.cleaned_data['location'],
                                'quantity': inventory_form.cleaned_data['quantity'],}

                    items = Inventory.objects.filter(name=inventory_form.cleaned_data['name'])
                    items_to_dict = [model_to_dict(i) for i in items]
                    shared_items = {k: form_data for k in form_data if k in items_to_dict and form_data == items_to_dict.values()}
                    location = Location.objects.all
                    print(location)
                    type = Type.objects.all
                    print(type)
                    for k in form_data.values():
                        print(k)
                    for k in items_to_dict:
                        print(k.values())
                    print(items_to_dict == form_data)
                    print("Shared Items", shared_items)

                    if (shared_items == {}):
                        ctxt['inventory_form'] = inventory_form
                        inventory_form.save()
                    else:
                        print("Running Dupe Code")
                        duplicate_line = Inventory.objects.get(id=items_to_dict['id'])
                        duplicate_line.quantity += inventory_form.cleaned_data['quantity']
                        duplicate_line.save()
            else:
                ctxt['inventory_form'] = inventory_form

        elif 'category' in request.POST:
            category_form = CategoryForm(request.POST)

            if category_form.is_valid():
                category_form.save()
            else:
                ctxt['category_form'] = category_form
        return render(request, self.template_name, self.get_context_data(**ctxt))

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name='Administrator').exists():
        return redirect('dashboard-index')
    users = UserProfile.objects.all()
    locations = Location.objects.all()
    context = {'users': users, 'locations': locations}
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def update_user_location(request, user_id):
    if not request.user.groups.filter(name='Administrator').exists():
        return redirect('dashboard-index')
    user_profile = UserProfile.objects.get(user__id=user_id)
    if request.method == 'POST':
        location_id = request.POST.get('location')
        location = Location.objects.get(id=location_id)
        user_profile.location = location
        user_profile.save()
        return redirect('dashboard-admin')
    locations = Location.objects.all()
    context = {'user_profile': user_profile, 'locations': locations}
    return render(request, 'dashboard/update_user_location.html', context)

class DeliveryList(LoginRequiredMixin, ListView):
    model = Delivery
    context_object_name = "delivery"

    def get_context_data(self, **kwargs):
        delivery = Delivery.objects.all()
        kwargs['delivery'] = delivery
        filteredDelivery = delivery.filter(deliveryLocation=self.request.user.userprofile.location)
        kwargs['filteredDelivery'] = filteredDelivery
        return kwargs
    
class QuotationList(LoginRequiredMixin, ListView):
    model = Quotation
    context_object_name = "quotation"

    def get_context_data(self, **kwargs):
        quotation = Quotation.objects.all()
        kwargs['quotation'] = quotation
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

@login_required
def approveDelivery(request):
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            delivery = Delivery.objects.filter(id__icontains=pk).first()
            if delivery:
                context = {'ord': delivery}
                if delivery.dateApproved is None:
                    delivery.dateApproved = datetime.datetime.now(datetime.timezone.utc)
                    delivery.save()
                return redirect('list-deliveries')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")

@login_required
@transaction.atomic
def arriveDelivery(request):
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            delivery = Delivery.objects.filter(id__icontains=pk).first()
            if delivery:
                context = {'ord': delivery}
                if delivery.dateArrived is None:
                    delivery.dateArrived = datetime.datetime.now(datetime.timezone.utc)
                    delivery.save()
                    
                    # update inventory items
                    for item in delivery.deliveryitem_set.all():
                        inventory_item = item.inventory
                        inventory_item.quantity += item.quantity
                        inventory_item.save()

                return redirect('list-deliveries')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")

@login_required
def delivery_batch_details(request, pk):
    deliverybatch = get_object_or_404(Delivery, pk=pk)
    deliverybatchInventoryitems = DeliveryItem.objects.filter(delivery=deliverybatch)
    context = {
        'deliverybatch': deliverybatch,
        'deliverybatchInventoryitems': deliverybatchInventoryitems,
        'pk': pk
    }
    return render(request, 'dashboard/delivery_details.html', context)

@login_required
def delivery_create_view(request):
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST or None)
        delivery_item_formset = DeliveryItemFormSet(request.POST or None, prefix='items')
        if delivery_form.is_valid() and delivery_item_formset.is_valid():
            delivery = delivery_form.save(commit=False)
            delivery.requestedBy = request.user
            delivery.deliveryLocation = request.user.userprofile.location
            delivery.save()  # save the delivery object first
            delivery_item_formset.instance = delivery  # set the delivery object as the instance for the formset
            # Filter inventory items based on the user's location
            inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
            for form in delivery_item_formset:
                form.fields['inventory'].queryset = inventory_items
            delivery_item_formset.save()  # then save the delivery item formset
            return redirect('list-deliveries')
    else:
        delivery_form = DeliveryForm()
        delivery_item_formset = DeliveryItemFormSet(prefix='items')
        # Filter inventory items based on the user's location
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        for form in delivery_item_formset:
            form.fields['inventory'].queryset = inventory_items
    return render(request, 'dashboard/create_delivery.html', {'delivery_form': delivery_form, 'delivery_item_formset': delivery_item_formset})

@login_required
def quotation_details(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    context = {
        'quotation': quotation,
        'quotation_items': quotation_items,
        'pk': pk,
    }
    return render(request, 'dashboard/quotation_details.html', context)


@login_required
def edit_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)

    if request.method == 'POST':
        formset = QuotationItemFormSet(request.POST, instance=quotation)
        form = QuotationForm(request.POST, instance=quotation)
        if formset.is_valid():
            formset_instances = formset.save(commit=False)
            for formset_instance, form in zip(formset_instances, formset.forms):
                if form.is_valid():
                    print('pls work')
                    quotation_item = formset_instance
                    quotation_item.quotation = quotation
                    quotation_item.save()
            formset.save_m2m()
            form.save()
            return redirect('quotation_details', pk=quotation.id)
        else:
            # check for fo rmset errors
            for subform in formset:
                if subform.errors:
                    print(subform.errors)
            print(formset.errors)
    else:
        form = QuotationForm(instance=quotation)
        formset = QuotationItemFormSet(instance=quotation)
    context = {
        'form': form,
        'formset': formset,
        'pk': pk,
    }
    print("HELLO???")
    return render(request, 'dashboard/edit_quotation.html', context) 


@login_required
def delete_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)

    if request.method == 'POST':
        quotation_items.delete()
        quotation.delete()
        return redirect('list-quotations', pk=quotation.delivery.id)
    
    else:
        return HttpResponse("Error.")

@login_required
def approveDelivery(request):
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            delivery = Delivery.objects.filter(id__icontains=pk).first()
            if delivery:
                context = {'ord': delivery}
                if delivery.dateApproved is None:
                    delivery.dateApproved = datetime.datetime.now(datetime.timezone.utc)
                    delivery.save()
                return redirect('list-deliveries')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")
    
@login_required
def approveQuotation(request):
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            delivery = Delivery.objects.filter(id__icontains=pk).first()
            if delivery:
                context = {'ord': delivery}
                if delivery.dateApproved is None:
                    delivery.dateApproved = datetime.datetime.now(datetime.timezone.utc)
                    delivery.save()
                return redirect('list-deliveries')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")

@login_required
def approve_quotation(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            pk = request.POST.get('pk')
            if pk:
                quotation = Quotation.objects.filter(id=pk).first()
                if quotation:
                    if quotation.dateApproved is None:
                        quotation.dateApproved = datetime.datetime.now(datetime.timezone.utc)
                        quotation.approvedBy = request.user
                        quotation.save()
                    return redirect('list-quotations')
                else:
                    return HttpResponse("Quotation not found.")
            else:
                return HttpResponse("No quotation ID specified.")
        else:
            return HttpResponse("You must be logged in to perform this action.")
    else:
        return HttpResponse("NOT POST")

@login_required
def quotation_create_view(request, pk):
    delivery = Delivery.objects.get(pk=pk)
    delivery_items = delivery.deliveryitem_set.all() # get all delivery items related to this delivery
    delivery_item_data = [{'inventory': item.inventory, 'quantity': item.quantity} for item in delivery_items]
    # create list of dictionaries with inventory and quantity data
    QuotationItemFormSet = inlineformset_factory(Quotation, QuotationItem, form=QuotationItemForm, extra=len(delivery_items))
    # generate formset with extra forms equal to the number of delivery items
    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST or None)
        quotation_item_formset = QuotationItemFormSet(request.POST or None, prefix='items', initial=delivery_item_data)
        # initialize formset with the delivery item data
        if quotation_form.is_valid() and quotation_item_formset.is_valid():
            quotation = quotation_form.save(commit=False)
            quotation.createdBy = request.user
            quotation.delivery = delivery
            quotation.save() 
            quotation_item_formset.instance = quotation  
            quotation_item_formset.save() 
            return redirect('list-quotations', pk=delivery.id)
    else:
        quotation_form = QuotationForm()
        quotation_item_formset = QuotationItemFormSet(prefix='items', initial=delivery_item_data)
        # initialize formset with the delivery item data
    return render(request, 'dashboard/create_quotation.html', {'quotation_form': quotation_form, 'quotation_item_formset': quotation_item_formset, 'pk': pk})

