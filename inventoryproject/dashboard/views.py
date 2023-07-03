import datetime
import pandas as pd
from django.forms import model_to_dict, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
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
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import F
from django.forms import formset_factory
from django.utils import timezone

# P.S. path has to be reflected also in urls.py
@login_required
def index(request):
    users_without_location = UserProfile.objects.exclude(location__isnull=False)
    inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
    restock_items = inventory_items.filter(quantity__lt=F('restocking_threshold'))
    delivery_items = DeliveryItem.objects.all()
    arriving_delivery = delivery_items.filter(deliveryLocation=request.user.userprofile.location, dateArrived__isnull=True)
    damaged_inventory = InventoryDamaged.objects.all()
    filtered_damaged_inventory = damaged_inventory.filter(verified_by__isnull=True,location=request.user.userprofile.location)
    inventory_returned = InventoryReturned.objects.all()
    query = Q(arrivalDate__isnull=True)
    query.add(Q(received_by__isnull=True), Q.AND)
    query.add(Q(transferredTo=request.user.userprofile.location), Q.AND)
    flitered_inventory_returned = inventory_returned.filter(query)
    request_pending = PurchaseRequest.objects.filter(dateApproved__isnull=True)
    request_delivery = PurchaseRequest.objects.filter(Q(approvedDelivery=False))
    today = timezone.now().date()
    delivery_today = delivery_items.filter(dateArrived__date=today)
    request_approval = PurchaseRequest.objects.filter(Q(approvedQuotations=False))

    context ={
        'users_without_location': users_without_location,
        'restock_items': restock_items,
        'arriving_delivery': arriving_delivery,
        'filtered_damaged_inventory': filtered_damaged_inventory,
        'flitered_inventory_returned': flitered_inventory_returned,
        'request_pending': request_pending,
        'request_delivery': request_delivery,
        'delivery_today': delivery_today,
        'request_approval': request_approval,
    }
    return render(request, 'dashboard/index.html', context)

class inventoryView(LoginRequiredMixin, View):
    template_name = 'dashboard/inventory.html'
    def get_context_data(self, **kwargs):
        if not self.request.user.userprofile.location:
            return redirect('dashboard-index')
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
        if not self.request.user.userprofile.location:
            return redirect('dashboard-index')
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}
        print(request.POST)
        if 'inventory' in request.POST:
            print("running request")
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

        return render(request, self.template_name, self.get_context_data(**ctxt))

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name='Administrator').exists():
        return redirect('dashboard-index')
    users = UserProfile.objects.all()
    locations = Location.objects.all()
    groups = Group.objects.all()
    context = {'users': users, 'locations': locations, 'groups': groups, 'category_form': CategoryForm()}
    
    if 'category' in request.POST:
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            category_form.save()
        else:
            context['category_form'] = category_form
    
    if 'add_group' in request.POST:
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        user.groups.add(group)
        
    if 'remove_group' in request.POST:
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        user.groups.remove(group)
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def update_user_location(request, user_id):
    if not request.user.groups.filter(name='Administrator').exists():
        return redirect('dashboard-index')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        location_id = request.POST['location']
        user_profile = UserProfile.objects.get(user=user)
        user_profile.location_id = location_id
        user_profile.save()
        return redirect('dashboard-admin')
    else:
        locations = Location.objects.all()
        return render(request, 'update_user_location.html', {'user': user, 'locations': locations})

@login_required
def update_user_groups(request, user_id):
    if not request.user.groups.filter(name='Administrator').exists():
        return redirect('dashboard-index')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        add_group_id = request.POST.get('add_group')
        if add_group_id:
            group = Group.objects.get(id=add_group_id)
            user.groups.add(group)
        remove_group_id = request.POST.get('remove_group')
        if remove_group_id:
            group = Group.objects.get(id=remove_group_id)
            user.groups.remove(group)
        return redirect('dashboard-admin')
    else:
        groups = Group.objects.all()
        return render(request, 'update_user_groups.html', {'user': user, 'groups': groups})

@login_required
def edit_inventory(request):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    inventory = Inventory.objects.filter(location=request.user.userprofile.location)
    context = {'inventory': inventory}
    return render(request, 'dashboard/edit_inventory.html', context)

@login_required
def update_inventory_restocking(request, inventory_id):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    inventory = Inventory.objects.get(id=inventory_id)
    if request.method == 'POST':
        if request.POST.get('restocking_threshold'):
            restocking_threshold = request.POST.get('restocking_threshold')
            inventory.restocking_threshold = restocking_threshold
        elif request.POST.get('restocking_amount'):
            restocking_amount = request.POST.get('restocking_amount')
            inventory.restocking_amount = restocking_amount
        inventory.save()
        return redirect('edit_inventory')
    context = {'inventory': inventory}
    return render(request, 'dashboard/edit_inventory.html', context)

# =============================== LIST VIEWS ========================
class DeliveryList(LoginRequiredMixin, ListView):
    model = DeliveryItem
    context_object_name = "deliveryItems"
    template_name = "dashboard/delivery_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deliveryItem = DeliveryItem.objects.all()
        dI = deliveryItem.filter(
            deliveryLocation=self.request.user.userprofile.location,
            dateArrived__isnull=True
        )
        context['deliveryItem'] = dI
        filteredDeliveryItem = deliveryItem.filter(
            deliveryLocation=self.request.user.userprofile.location,
            dateArrived__isnull=False
        )
        context['filteredDeliveryItem'] = filteredDeliveryItem
        return context
    
    def get(self, request, *args, **kwargs):
        if not self.request.user.userprofile.location:
            return redirect('dashboard-index')
        return super().get(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class QuotationList(ListView):
    model = Quotation
    context_object_name = "quotation"

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
            return redirect('dashboard-index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the purchase request instance for the given pk
        purchase_request = get_object_or_404(PurchaseRequest, pk=self.kwargs['pk'])
        # filter the quotation items based on the purchase request instance
        quotationItem = QuotationItem.objects.filter(quotation__purchaseRequest=purchase_request)
        context['quotationItem'] = quotationItem
        context['pRequest'] = purchase_request
        context['pk'] = self.kwargs['pk']
        context['today'] =  datetime.datetime.now(datetime.timezone.utc)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # get the quotation item to be approved
            pk = request.POST.get('pk')
            quotation_item = get_object_or_404(QuotationItem, pk=pk)

            # render the delivery form
            return render(request, 'delivery_form.html', {'quotation_item': quotation_item})
        return super().get(request, *args, **kwargs)

class RequestList(LoginRequiredMixin, ListView):
    model = PurchaseRequest
    context_object_name = "pRequest"
    template_name = "dashboard/request_list.html" 

    def get_context_data(self, **kwargs):
        pRequest = PurchaseRequest.objects.filter(Q(approvedDelivery=False) | Q(confirmedDeliveryCount__lt=F('totalDeliveryCount')))
        filteredRequest = PurchaseRequest.objects.filter(approvedDelivery=True)

        for request in reversed(filteredRequest):
            
            if request.confirmedDeliveryCount != request.totalDeliveryCount:
                filteredRequest = filteredRequest.exclude(pk=request.pk)
                pRequest = pRequest | PurchaseRequest.objects.filter(pk=request.pk)
                
        kwargs['pRequest'] = pRequest
        kwargs['filteredRequest'] = filteredRequest
        kwargs['today'] =  datetime.datetime.now(datetime.timezone.utc)

        return super().get_context_data(**kwargs)
    
    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
            return redirect('dashboard-index')
        return super().get(request, *args, **kwargs)


# =========================== DELIVERY VIEWS ======================================
from django.contrib import messages

@login_required
def createRequest(request):
    if request.method == 'POST':
        print("RUNNING POST: ", request.POST)
        RequestItemFormSet = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=1, can_delete=False, can_delete_extra=True)
        requestForm = RequestForm(request.POST or None)
        requestItemFormset = RequestItemFormSet(request.POST or None, prefix='items')
        requestItemFormsetEmpty = RequestItemFormSet(prefix='items')
        if requestForm.is_valid() and requestItemFormset.is_valid():
            pRequest = requestForm.save(commit=False)
            pRequest.requestedBy = request.user
            pRequest.requestLocation = request.user.userprofile.location
            identical_items = []
            for form in requestItemFormset:
                identical_requests = PurchaseRequest.objects.filter(
                    requestLocation=pRequest.requestLocation,
                    purchase_request_items__inventory=form.cleaned_data['inventory']
                ).exclude(approvedDelivery=True)
                if identical_requests.exists():
                    identical_items.append(str(form.cleaned_data['inventory']))
            if identical_items:
                message = 'The following items already exist in an identical purchase request and have not been approved for delivery: {}'.format(", ".join(identical_items))
                messages.warning(request, message)
                inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
                restock_items = inventory_items.filter(quantity__lt=F('restocking_threshold'))
                initial_data=[]
                for item in  restock_items:
                    initial_data.append({'inventory': item.id, 'quantity': item.restocking_amount - item.quantity})
                
                requestForm = RequestForm()
                RequestItemFormSet = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=len(initial_data), can_delete=False, can_delete_extra=True)
                RequestItemFormSetEmpty = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=1, can_delete=False, can_delete_extra=True)
                
                requestItemFormset = RequestItemFormSet(prefix='items')
                requestItemFormsetEmpty = RequestItemFormSetEmpty(prefix='items')
                for form in requestItemFormset:
                        form.fields['inventory'].queryset = inventory_items
                for form in requestItemFormsetEmpty:
                        form.fields['inventory'].queryset = inventory_items
            else: 
                print("REQ ITEMFORMSET: ", requestItemFormset)
                pRequest.save()  # save the delivery object first
                requestItemFormset.instance = pRequest  # set the delivery object as the instance for the formset

                # Save each purchase request item separately
                for form in requestItemFormset:
                    item = form.save(commit=False)
                    item.purchaseRequest = pRequest
                    print("ITEM", item)
                    item.save()
                    print("POST FINISH")

                return redirect('list-deliveries')
    else:
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        restock_items = inventory_items.filter(quantity__lt=F('restocking_threshold'))
        initial_data=[]
        for item in  restock_items:
            initial_data.append({'inventory': item.id, 'quantity': item.restocking_amount - item.quantity})

        requestForm = RequestForm()
        RequestItemFormSet = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=1, can_delete=False, can_delete_extra=True)
        RequestItemFormSetEmpty = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=1, can_delete=False, can_delete_extra=True)

        requestItemFormset = RequestItemFormSet(prefix='items')
        requestItemFormsetEmpty = RequestItemFormSetEmpty(prefix='items')

        for form in requestItemFormset:
            form.fields['inventory'].queryset = inventory_items

        for form in requestItemFormsetEmpty:
            form.fields['inventory'].queryset = inventory_items
        

        if request.GET.get('restock'):
            RequestItemFormSet = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=len(initial_data), can_delete=False, can_delete_extra=True)
            requestItemFormset = RequestItemFormSet(initial=initial_data, prefix='items')
            for form in requestItemFormset:
                print("")
                form.fields['inventory'].queryset = inventory_items
            for form in requestItemFormsetEmpty:
                print("")
                form.fields['inventory'].queryset = inventory_items
    return render(request, 'dashboard/create_request.html', {'requestForm': requestForm, 'requestItemFormset': requestItemFormset, 'requestItemFormsetEmpty': requestItemFormsetEmpty})




@login_required
def create_delivery(request):
    if request.method == 'POST':
        quotation_item_pk = request.POST.get('pk')
        expected_delivery_date = request.POST.get('expected_date')
        print("expected_delivery_date: ", expected_delivery_date)

        # get the quotation item and create the delivery and delivery item objects
        quotation_item = get_object_or_404(QuotationItem, id=quotation_item_pk)
        pRequest = quotation_item.quotation.purchaseRequest
        pRequest.approvedDelivery = True
        pRequest.confirmedDeliveryCount += 1
        pRequest.save()
        quotation_item.deliverySet = True
        quotation_item.save()
        DeliveryItem.objects.create(
            inventory=quotation_item.inventory,
            quotationItem=quotation_item,
            quantity=quotation_item.quantity,
            dateApproved=datetime.datetime.now(datetime.timezone.utc),
            approvedBy=request.user,
            expectedDeliveryDate=expected_delivery_date,
            deliveryLocation=quotation_item.quotation.purchaseRequest.requestLocation,
        )

        return HttpResponseRedirect(reverse('list-deliveries'))
    else:
        return HttpResponse("NOT POST")
# =========================== QUOTATION VIEWS ================================
@login_required
def quotation_details(request, pk):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
        return redirect('dashboard-index')
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    context = {
        'quotation': quotation,
        'quotation_items': quotation_items,
        'pk': pk,
    }
    return render(request, 'dashboard/quotation_details.html', context)

@login_required
def quotation_create_view(request, pk):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
        return redirect('dashboard-index')
    pRequest = PurchaseRequest.objects.get(pk=pk)
    requestItems = pRequest.purchase_request_items.all() # get all delivery items related to this delivery
    requestItemsData = [{'inventory': item.inventory, 'quantity': item.quantity} for item in requestItems]
    # create list of dictionaries with inventory and quantity data
    QuotationItemFormSet = inlineformset_factory(Quotation, QuotationItem, form=QuotationItemForm, extra=len(requestItems))
    # generate formset with extra forms equal to the number of delivery items
    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST or None)
        quotation_item_formset = QuotationItemFormSet(request.POST or None, prefix='items', initial=requestItemsData)
        # initialize formset with the delivery item data
        if quotation_form.is_valid() and quotation_item_formset.is_valid():
            quotation = quotation_form.save(commit=False)
            quotation.createdBy = request.user
            pRequest.approvedBy = request.user
            if (pRequest.dateApproved is None):
                pRequest.dateApproved = datetime.datetime.now(datetime.timezone.utc)
            quotation.purchaseRequest = pRequest
            pRequest.save()
            quotation.save() 
            quotation_item_formset.instance = quotation  
            quotation_item_formset.save() 
            return redirect('list-quotations', pk=pRequest.id)
    else:
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        quotation_form = QuotationForm()
        quotation_item_formset = QuotationItemFormSet(prefix='items', initial=requestItemsData)
        quotation_item_formset_empty = QuotationItemFormSet(prefix='items')
        # initialize formset with the delivery item data
        for form in quotation_item_formset:
                form.fields['inventory'].queryset = inventory_items
        for form in quotation_item_formset_empty:
                form.fields['inventory'].queryset = inventory_items
    return render(request, 'dashboard/create_quotation.html', {'quotation_form': quotation_form, 'quotation_item_formset': quotation_item_formset, 'quotation_item_formset_empty': quotation_item_formset_empty, 'pk': pk})

@login_required
def edit_quotation(request, pk):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
        return redirect('dashboard-index')
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
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
        return redirect('dashboard-index')
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)

    if request.method == 'POST':
        quotation_items.delete()
        quotation.delete()
        return redirect('list-quotations', pk=quotation.delivery.id)
    
    else:
        return HttpResponse("Error.")

# =============================== APPROVE AND ARRIVE ========================

@login_required
def approveQuotation(request):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists():
        return redirect('dashboard-index')
    if request.method == 'POST':
        if request.user.is_authenticated:
            pk = request.POST.get('pk')
            if pk:
                quotation = QuotationItem.objects.filter(id=pk).first()
                if quotation:
                    if quotation.dateApproved is None:
                        quotation.dateApproved = datetime.datetime.now(datetime.timezone.utc)
                        quotation.approvedBy = request.user
                        purchase_request = quotation.quotation.purchaseRequest
                        purchase_request.approvedQuotations = True
                        print(purchase_request.totalDeliveryCount)
                        purchase_request.totalDeliveryCount += 1
                        
                        purchase_request.save()
                        quotation.save()
                    return redirect('list-quotations', pk=quotation.quotation.purchaseRequest.id)
                else:
                    return HttpResponse("Quotation not found.")
            else:
                return HttpResponse("No quotation ID specified.")
        else:
            return HttpResponse("You must be logged in to perform this action.")
    else:
        return HttpResponse("NOT POST")

from django.forms import formset_factory

@login_required
def create_partial_delivery(request, pk):
    qItem = QuotationItem.objects.get(pk=pk)
    PartialDeliveryFormSet = formset_factory(PartialDeliveryForm, extra=1)
    
    if request.method == 'POST':
        formset = PartialDeliveryFormSet(request.POST, prefix='formset')
        print(formset)
        if formset.is_valid():
            i = 0
            for form in formset:
                i += 1
                print("I value: ", i)
                expected_delivery_date = form.cleaned_data['expectedDeliveryDate']
                pQuantity = form.cleaned_data['pQuantity']
                pRequest = qItem.quotation.purchaseRequest
                pRequest.approvedDelivery = True
                pRequest.confirmedDeliveryCount += 1
                if pRequest.totalDeliveryCount == 0:
                    pRequest.totalDeliveryCount += 1
                    print("ONLY ONCE")
                if i > 1:
                    pRequest.totalDeliveryCount += 1
                    print("WE RAN")
                    print("value: ", pRequest.totalDeliveryCount)
                pRequest.save()
                qItem.deliverySet = True
                qItem.save()
                
                DeliveryItem.objects.create(
                    inventory=qItem.inventory,
                    quotationItem=qItem,
                    quantity=qItem.quantity,
                    dateApproved=datetime.datetime.now(datetime.timezone.utc),
                    approvedBy=request.user,
                    deliveryLocation=qItem.quotation.purchaseRequest.requestLocation,
                    expectedDeliveryDate=expected_delivery_date,
                    pQuantity=pQuantity
                )
            return HttpResponseRedirect(reverse('list-deliveries'))
        else:
            print("uh oh")
            for form in formset:
                print(form)
    else:
        formset = PartialDeliveryFormSet(prefix='formset')

    context = {'formset': formset, 'qItem': qItem, 'today': datetime.datetime.now(datetime.timezone.utc)}
    return render(request, 'dashboard/create_partial_delivery.html', context)


@login_required
@transaction.atomic
def arriveDelivery(request):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            delivery = DeliveryItem.objects.filter(id__icontains=pk).first()
            if delivery:
                context = {'ord': delivery}
                if delivery.dateArrived is None:
                    delivery.dateArrived = datetime.datetime.now(datetime.timezone.utc)
                    delivery.save()

                    inventory_item = delivery.inventory
                    if delivery.pQuantity > 0:
                        inventory_item.quantity += delivery.pQuantity
                    else:
                        inventory_item.quantity += delivery.quantity
                    inventory_item.save()

                return redirect('list-deliveries')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")
    
# ============================ WITHDRAW INVENTORY ===========================

@login_required
def inventory_withdrawals(request):
    if not request.user.userprofile.location:
            return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Engineering').exists():
        print("uh oh")
        return redirect('dashboard-index')
    inventory_withdrawals = InventoryWithdrawn.objects.all()
    return render(request, 'dashboard/inventory_withdrawals.html', {'inventory_withdrawals': inventory_withdrawals})

@login_required
def inventory_withdraw(request):
    if not request.user.userprofile.location:
            return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    formset = InventoryWithdrawnFormSet(request.POST or None, queryset=InventoryWithdrawn.objects.none())
    print(request.POST)
    if request.method == 'POST':
        if formset.is_valid():
            instances = formset.save(commit=False)
            print(instances)
            for instance in instances:
                print(instance)
                inventory = instance.inventory
                quantity = instance.quantity
                if inventory.quantity >= quantity:
                    inventory.quantity -= quantity
                    inventory.save()
                    instance.withdrawn_by = request.user
                    instance.save()
                else:
                    return redirect('inventory_withdraw')
            messages.success(request, 'Inventory withdrawn successfully.')
            return redirect('inventory_withdrawals')
    else:
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        for form in formset:
                form.fields['inventory'].queryset = inventory_items
    return render(request, 'dashboard/inventory_withdraw.html', {'formset': formset})

@login_required
def inventory_returned(request):
    if not request.user.userprofile.location:
        return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(
            name='Engineering').exists():
        return redirect('dashboard-index')
    inventory_returned = InventoryReturned.objects.all()
    query = Q(arrivalDate__isnull=True)
    query.add(Q(received_by__isnull=True), Q.AND)
    query.add(Q(transferredFrom=request.user.userprofile.location), Q.AND)
    query.add(Q(transferredTo=request.user.userprofile.location), Q.OR)

    flitered_inventory_returned = inventory_returned.filter(query)
    destination_locations = Location.objects.exclude(name=request.user.userprofile.location)
    return render(request, 'dashboard/inventory_returns.html', {'inventory_returned': inventory_returned, 'flitered_inventory_returned': flitered_inventory_returned, 'destination_locations': destination_locations})

@login_required
def inventory_return(request):
    if not request.user.userprofile.location:
        return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(
            name='Engineering').exists():
        return redirect('dashboard-index')
    form = InventoryReturnedForm(request.POST or None)
    formset = InventoryReturnedFormSet(request.POST or None, queryset=InventoryReturned.objects.none())
    if request.method == 'POST':
        print("posting")
        if formset.is_valid():
            print("valid")
            instances = formset.save(commit=False)
            for instance in instances:
                instance.transferred_by = request.user
                instance.transferredFrom = request.user.userprofile.location
                instance.save()
                return redirect('inventory_returned')   
        else:
            print(form.errors)
            print(form)
    else:
        locations = Location.objects.exclude(name=request.user.userprofile.location)
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        for form in formset:
            form.fields['inventory'].queryset = inventory_items
            form.fields['transferredTo'].queryset = locations
            
    return render(request, 'dashboard/inventory_return.html', {'formset': formset})

@login_required
def inventory_return_all(request):
    if not request.user.userprofile.location:
        return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(
            name='Engineering').exists():
        return redirect('dashboard-index')
    source_location = request.user.userprofile.location
    target_location_id = request.POST.get('targetLocation')
    if target_location_id:
        try:
            target_location = Location.objects.get(id=target_location_id)
            inventory_items = Inventory.objects.filter(location=source_location)
            for item in inventory_items:
                InventoryReturned.objects.create(
                    inventory=item,
                    quantity=item.quantity,
                    transferred_by=request.user,
                    transferredFrom=source_location,
                    transferredTo=target_location,
                    transferDate=datetime.datetime.now(datetime.timezone.utc)
                )
            return redirect('inventory_returned')
        except Location.DoesNotExist:
            return HttpResponse("Invalid target location.")
    return render(request, 'dashboard/inventory_returns.html')

def receive_transfer(request):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            returned_item = InventoryReturned.objects.get(id=pk)
            if returned_item:
                if returned_item.arrivalDate is None:
                    returned_item.arrivalDate = datetime.datetime.now(datetime.timezone.utc)
                    
                    transferred_quantity = returned_item.quantity
                    transferred_from = returned_item.transferredFrom
                    transferred_to = returned_item.transferredTo
                    inventory_name = returned_item.inventory.name

                    # Update the inventory quantity for the source location
                    inventory_source = Inventory.objects.get(location=transferred_from, name=inventory_name)
                    inventory_source.quantity -= transferred_quantity
                    print("Source: ", inventory_source)
                    inventory_source.save()

                    # Get or create the inventory item at the destination location
                    inventory_destination, created = Inventory.objects.get_or_create(
                        name=inventory_name,
                        type=inventory_source.type,
                        location=transferred_to,
                        defaults={
                            'quantity': transferred_quantity,
                            'restocking_threshold': inventory_source.restocking_threshold,
                            'restocking_amount': inventory_source.restocking_amount
                        }
                    )

                    if not created:
                        inventory_destination.quantity += transferred_quantity
                        print("its alive")
                        inventory_destination.save()
                    print("Destination: ", inventory_destination)

                    returned_item.save()

                return redirect('inventory_returned')
            else:
                return HttpResponse("Order not found.")
        else:
            return HttpResponse("No order ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")
    
def delete_transfer(request, pk):
    transfer = InventoryReturned.objects.get(pk=pk)
    transfer.delete()
    return redirect('inventory_returned')

def damaged_inventory(request):
    if not request.user.userprofile.location:
        return redirect('dashboard-index')
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    form = InventoryDamagedForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            inventory_damaged = form.save(commit=False)
            inventory_damaged.created_by = request.user
            inventory_damaged.location = request.user.userprofile.location
            inventory_damaged.reported_date = datetime.datetime.now(datetime.timezone.utc)
            inventory_damaged.save()
            return redirect('damaged_inventory')
    else:
        form = InventoryDamagedForm()
        inventory_items = Inventory.objects.filter(location=request.user.userprofile.location)
        form.fields['inventory'].queryset = inventory_items
    
    damaged_inventory = InventoryDamaged.objects.all()
    filtered_damaged_inventory = InventoryDamaged.objects.filter(
        verified_by__isnull=True,
        location=request.user.userprofile.location
    )

    context = {
        'form': form,
        'damaged_inventory': damaged_inventory,
        'filtered_damaged_inventory': filtered_damaged_inventory
    }
    return render(request, 'dashboard/damaged_inventory.html', context)

def delete_damage(request, pk):
    dmg = InventoryDamaged.objects.get(pk=pk)
    dmg.delete()
    return redirect('damaged_inventory')

def verify_damage(request):
    if not request.user.groups.filter(name='Administrator').exists() and not request.user.groups.filter(name='Finance').exists() and not request.user.groups.filter(name='Management').exists() and not request.user.groups.filter(name='Engineering').exists():
        return redirect('dashboard-index')
    
    if request.user.is_authenticated:
        pk = request.POST.get('pk') if request.POST.get('pk') else None
        if pk:
            damaged_item = InventoryDamaged.objects.get(id=pk)
            if damaged_item:
                if damaged_item.verified_date is None:
                    damaged_item.verified_date = datetime.datetime.now(datetime.timezone.utc)
                    damaged_item.verified_by = request.user
                    
                    inventory_name = damaged_item.inventory.name
                    damaged_from = damaged_item.location

                    # Update the inventory quantity for the source location
                    inventory_source = Inventory.objects.get(location=damaged_from, name=inventory_name)
                    inventory_source.quantity -= damaged_item.quantity
                    inventory_source.save()

                    damaged_item.save()

                return redirect('damaged_inventory')
            else:
                return HttpResponse("Damaged item not found.")
        else:
            return HttpResponse("No damaged ID specified.")
    else:
        return HttpResponse("You must be logged in to perform this action.")

import json

def import_data(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                return render(request, 'dashboard/import.html', {'form': form, 'error_message': 'Invalid file format'})
            
            required_columns = ['name', 'type', 'location', 'quantity']
            missing_columns = set(required_columns) - set(df.columns)

            if missing_columns:
                error_message = f"Missing columns: {', '.join(missing_columns)}"
                return render(request, 'dashboard/import.html', {'form': form, 'error_message': error_message})
            
            locations = Location.objects.all()
            types = Type.objects.all()

            # Iterate over the rows of the DataFrame and extract the necessary information
            preview_data = []
            missing_rows = []
            for index, row in df.iterrows():
                name = row['name']
                type_id = row['type']
                location_id = row['location']
                quantity = row['quantity']
                
                # Skip the row if any of the required fields are missing or NaN
                if pd.isna(name) or pd.isna(type_id) or pd.isna(location_id) or pd.isna(quantity):
                    missing_rows.append(index)
                    continue

                # Find the corresponding location and type objects based on their IDs
                location_obj = locations.get(id=location_id) if location_id else None
                location_name = location_obj.name if location_id else ''
                type_name = types.get(id=type_id).name if location_id else ''

                # Create a dictionary with the extracted data
                data = {
                    'name': name,
                    'type_id': type_id,
                    'type_name': type_name,
                    'location_id': location_id,
                    'location_name': location_name,
                    'quantity': quantity,
                    'restocking_threshold': row.get('restocking_threshold', 0),
                    'restocking_amount': row.get('restocking_amount', 0),
                }
                print("WAHT")
                # Add the dictionary to the preview_data list
                preview_data.append(data)

            if not preview_data:  # Check if preview_data is 
                print("WasdadsAHT")
                return render(request, 'dashboard/import.html', {'form': form, 'error_message': 'File does not have valid values'})
            # Convert preview_data to a JSON string
            preview_data_json = json.dumps(preview_data)

            # Store the preview_data and missing_rows in the session
            
            request.session['preview_data'] = preview_data_json
            request.session['missing_rows'] = missing_rows
            return redirect('import_confirm')
    else:
        form = FileUploadForm()
    return render(request, 'dashboard/import.html', {'form': form})



import json


def confirm_import(request):
    preview_data = request.session.get('preview_data')
    if not preview_data:
        return redirect('inventory_import')

    # Convert the JSON string to a list of dictionaries
    preview_data = json.loads(preview_data)

    # Get the locations and types from the database
    locations = Location.objects.all()
    types = Type.objects.all()

    # Convert the preview_data to a pandas DataFrame
    df = pd.DataFrame(preview_data)

    # Replace NaN values with 0 in the restocking_amount and restocking_threshold columns
    df['restocking_amount'].fillna(0, inplace=True)
    df['restocking_threshold'].fillna(0, inplace=True)

    # Convert the DataFrame back to a list of dictionaries
    updated_preview_data = df.to_dict(orient='records')

    if request.method == 'POST':
        # Save the data to the Inventory model
        for item in updated_preview_data:
            # Find the corresponding location and type objects based on their IDs
            location_id = item['location_id']
            location = locations.get(id=location_id)

            type_id = item['type_id']
            type = types.get(id=type_id)

            # Check if an inventory item with the same name and location exists
            existing_item = Inventory.objects.filter(name=item['name'], location=location).first()

            if existing_item:
                # If an existing item is found, update its quantity
                existing_item.quantity = F('quantity') + item['quantity']
                existing_item.save()
            else:
                # If no existing item is found, create a new inventory item
                inventory_item = Inventory(
                    name=item['name'],
                    type=type,  # Assign the type object
                    location=location,  # Assign the location object
                    quantity=item['quantity'],
                    restocking_threshold=item['restocking_threshold'],
                    restocking_amount=item['restocking_amount'],
                )
                inventory_item.save()

        # Clear the preview_data from the session
        del request.session['preview_data']

        return redirect('dashboard-inventory')

    return render(request, 'dashboard/confirm_import.html', {'preview_data': updated_preview_data, 'locations': locations, 'types': types})
