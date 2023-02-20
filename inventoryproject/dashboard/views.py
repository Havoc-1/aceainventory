import datetime
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Delivery, Location, Inventory, DeliveryItem, Type
from .forms import CategoryForm, DeliveryForm, InventoryForm, DeliveryItemForm, DeliveryItemFormSet
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db import transaction

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

class DeliveryList(ListView):
    model = Delivery
    context_object_name = "delivery"

    def get_context_data(self, **kwargs):
        delivery = Delivery.objects.all()
        kwargs['delivery'] = delivery
        return kwargs

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
        'deliverybatchInventoryitems': deliverybatchInventoryitems
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
            delivery_item_formset.save()  # then save the delivery item formset
            return redirect('list-deliveries')
    else:
        delivery_form = DeliveryForm()
        delivery_item_formset = DeliveryItemFormSet(prefix='items')
    return render(request, 'dashboard/create_delivery.html', {'delivery_form': delivery_form, 'delivery_item_formset': delivery_item_formset})

