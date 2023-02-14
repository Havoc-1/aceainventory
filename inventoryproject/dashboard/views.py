from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Delivery, Location, Product, DeliveryItem, Type
from .forms import CategoryForm, DeliveryForm, ProductForm, DeliveryItemForm, DeliveryItemFormSet
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# P.S. path has to be reflected also in urls.py
@login_required
def index(request):
    if 'searchBar' in request.GET:                          # Search Functionality
        searchBar = request.GET['searchBar']
        multiple_query = Q(Q(name__icontains=searchBar) | Q(location__icontains=searchBar))
        product = Product.objects.filter(multiple_query)
    else: 
        product = Product.objects.all                    # makes it so product can be viewed by non-staff (ENGINEERING)                
    context ={
        'product': product,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    return render(request, 'dashboard/staff.html')

class productView(LoginRequiredMixin, View):
    template_name = 'dashboard/inventory.html'
    def get_context_data(self, **kwargs):
        product = Product.objects.all
        kwargs['product'] = product
        if 'product_form' not in kwargs:
            kwargs['product_form'] = ProductForm()
        if 'category_form' not in kwargs:
            kwargs['category_form'] = CategoryForm()

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}
        print(request.POST)
        if 'product' in request.POST:
            product_form = ProductForm(request.POST)

            if product_form.is_valid():
                product_form.clean()
                prod = product_form.clean()
                print(prod)
                print(prod.get('location'))
                if request.method == 'POST':

                    print(request.POST.get('location'))
                    form_data = {'name': product_form.cleaned_data['name'],
                                'type': product_form.cleaned_data['type'],
                                'location': product_form.cleaned_data['location'],
                                'quantity': product_form.cleaned_data['quantity'],}

                    items = Product.objects.filter(name=product_form.cleaned_data['name'])
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
                        ctxt['product_form'] = product_form
                        product_form.save()
                    else:
                        print("Running Dupe Code")
                        duplicate_line = Product.objects.get(id=items_to_dict['id'])
                        duplicate_line.quantity += product_form.cleaned_data['quantity']
                        duplicate_line.save()
            else:
                ctxt['product_form'] = product_form

        elif 'category' in request.POST:
            category_form = CategoryForm(request.POST)

            if category_form.is_valid():
                category_form.save()
            else:
                ctxt['category_form'] = category_form
        return render(request, self.template_name, self.get_context_data(**ctxt))

class DeliveryList(ListView):
    model = Delivery
    template_name = "dashboard/delivery_list.html"
    context_object_name = "deliveries"
    deliveries = Delivery.objects.all

    def get_context_data(self, **kwargs):
        delivery = Delivery.objects.all
        kwargs['delivery'] = delivery

        return kwargs

def delivery_batch_details(request, pk):
    deliverybatch = get_object_or_404(Delivery, pk=pk)
    deliverybatchproducts = DeliveryItem.objects.filter(deliveryDetails=deliverybatch)
    context = {
        'deliverybatch': deliverybatch,
        'deliverybatchproducts': deliverybatchproducts
    }
    return render(request, 'dashboard/delivery_details.html', context)
    
def delivery_create_view(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        formset = DeliveryItemFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            delivery = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.delivery = delivery
                item.save()
            return redirect('delivery_list')
    else:
        form = DeliveryForm()
        formset = DeliveryItemFormSet(prefix='items')
    return render(request, 'create_delivery.html', {'form': form, 'formset': formset})