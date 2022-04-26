from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory
from .forms import InventoryForm
from django.contrib.auth.decorators import login_required

# P.S. path has to be reflected also in urls.py
@login_required
def index(request):
    inventory = Inventory.objects.all                    # makes it so inventory can be viewed by non-staff (ENGINEERING)

    context ={
        'inventory': inventory,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    return render(request, 'dashboard/staff.html')

@login_required
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

@login_required
def inventory_delete(request, pk):                          # pk stands for primary key
    item = Inventory.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-inventory')
    return render(request, 'dashboard/inventory_delete.html')

@login_required
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

@login_required
def deliveries(request):
    return render(request, 'dashboard/deliveries.html')