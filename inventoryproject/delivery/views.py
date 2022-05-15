from django.shortcuts import render, redirect
from .models import Delivery, Inventory
from django.http import HttpResponse
from .forms import DeliveryRequestForm, DeliveryRequestItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def index(request):
    delivery = Delivery.objects.all

    context ={
        'delivery': delivery,
    }
    return render(request, 'delivery/index.html', context)

@login_required
def details(request, pk):
    item = Delivery.objects.get(id=pk)

    context ={
        'item': item,
    }
    return render(request, 'delivery/details.html', context)

@login_required
def delivery_request(request):
    delivery = Delivery.objects.all                    # ORM Model (the one django uses), same as SQL but Inventory.objects.raw(SELECT * from dashboard_inventory)
    
    context ={
        'delivery': delivery,
    }
    return render(request, 'delivery/request.html', context)

class DeliveryRequestNew(LoginRequiredMixin, View):
    template_name = 'delivery/request_new.html'

    def get_context_data(self, **kwargs):
        if 'item_form' not in kwargs:
            kwargs['item_form'] = DeliveryRequestItemForm()
        if 'request_form' not in kwargs:
            kwargs['request_form'] = DeliveryRequestForm()

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}

        if 'item' in request.POST:
            item_form = DeliveryRequestItemForm(request.POST)

            if item_form.is_valid():
                item_form.save()
            else:
                ctxt['item_form'] = item_form

        elif 'request' in request.POST:
            request_form = DeliveryRequestForm(request.POST)

            if request_form.is_valid():
                request_form.save()
            else:
                ctxt['request_form'] = request_form

        return render(request, self.template_name, self.get_context_data(**ctxt))
        
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