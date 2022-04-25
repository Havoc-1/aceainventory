from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory
from .forms import InventoryForm

# P.S. path has to be reflected also in urls.py
def index(request):
    return render(request, 'dashboard/index.html')

def staff(request):
    return render(request, 'dashboard/staff.html')

def inventory(request):
    inventory = Inventory.objects.all                    # ORM Model (the one django uses), same as SQL but Inventory.objects.raw(SELECT * from dashboard_inventory)

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-inventory')
    else:
        form=InventoryForm()

    context ={
        'inventory': inventory,
        'form': form,
    }
    return render(request, 'dashboard/inventory.html', context)

def inventory_delete(request, pk):                          # pk stands for primary key
    item = Inventory.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-inventory')
    return render(request, 'dashboard/inventory_delete.html')

def inventory_edit(request, pk):                          # pk stands for primary key
    item = Inventory.objects.get(id=pk)
    if request.method=='POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():                                 
            form.save()                                     # shows the information from previous page
            return redirect('dashboard-inventory')          # redirects back to inventory
    else:
        form = InventoryForm(instance=item)
    context={
        'form': form,
    }
    return render(request, 'dashboard/inventory_edit.html', context)

def deliveries(request):
    return render(request, 'dashboard/deliveries.html')