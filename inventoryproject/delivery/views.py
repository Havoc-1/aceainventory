from django.shortcuts import render, redirect
from .models import Delivery, Inventory
from django.http import HttpResponse
from .forms import DeliveryRequestForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def add_to_delivery(request, inventory_id):
    delivery = Delivery(request)
    delivery.add(inventory_id)

    return render(request, 'delivery/menu_cart.html ')

def delivery_request(request):
    return render(request, 'delivery/delivery_request.html')

# HMMMM

@login_required
def index(request):
    return render(request, 'delivery/index.html')

@login_required
def details(request):
    return render(request, 'delivery/details.html')

@login_required
def delivery_request(request):
    delivery = Delivery.objects.all                    # ORM Model (the one django uses), same as SQL but Inventory.objects.raw(SELECT * from dashboard_inventory)
    
    context ={
        'delivery': delivery,
    }
    return render(request, 'delivery/request.html', context)

@login_required
def delivery_request_new(request):
    delivery = Delivery.objects.all                    # ORM Model (the one django uses), same as SQL but Inventory.objects.raw(SELECT * from dashboard_inventory)

    if request.method == 'POST':
        form = DeliveryRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('delivery-request')
    else:
        form=DeliveryRequestForm()
    
    context ={
        'delivery': delivery,
        'form': form,
    }
    return render(request, 'delivery/request_new.html', context)

@login_required
def delivery_request_edit(request, pk):                          # pk stands for primary key
    item = Delivery.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('delivery-request')
    return render(request, 'delivery/request_delete.html')

@login_required
def delivery_request_edit(request, pk):                          # pk stands for primary key
    item = Delivery.objects.get(id=pk)
    if request.method=='POST':
        form = DeliveryRequestForm(request.POST, instance=item)
        if form.is_valid():                                 
            form.save()                                     # shows the information from previous page
            return redirect('delivery-request')          # redirects back to inventory
    else:
        form = DeliveryRequestForm(instance=item)
    context={
        'form': form,
    }
    return render(request, 'delivery/request_edit.html', context)