from django import forms
from django.forms import inlineformset_factory
from .models import Delivery, Inventory, DeliveryItem, Type

class InventoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        abstract = True
        model = Inventory
        fields = ['name', 'location', 'type', 'quantity',]
        
class CategoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Type
        fields = ['name',]

# ========================================= DELIVERY FORMS =============================================== #

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        exclude = ['requestedBy', 'deliveryLocation', 'dateApproved', 'dateArrived']

class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = '__all__'
        
DeliveryItemFormSet = inlineformset_factory(Delivery, DeliveryItem, form=DeliveryItemForm, extra=1, can_delete=False, can_delete_extra=True)

# DELIVERY UPDATE FORMS
class UpdateDateArrivedForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['dateArrived']

    def update_date_arrived(request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        if request.method == 'POST':
            form = UpdateDateArrivedForm(request.POST, instance=delivery)
            if form.is_valid():
                delivery.update_dateArrived(form.cleaned_data['dateArrived'])
                return redirect('delivery_list')
        else:
            form = UpdateDateArrivedForm(instance=delivery)
        return render(request, 'update_date_arrived.html', {'form': form})


class UpdateDateApprovedForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['dateApproved']

    def update_date_approved(request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        if request.method == 'POST':
            form = UpdateDateApprovedForm(request.POST, instance=delivery)
            if form.is_valid():
                delivery.update_dateApproved(form.cleaned_data['dateApproved'])
                return redirect('delivery_list')
        else:
            form = UpdateDateApprovedForm(instance=delivery)
        return render(request, 'update_date_approved.html', {'form': form})

# ======================================================================================================== #

