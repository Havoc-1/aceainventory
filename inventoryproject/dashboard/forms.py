from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseRequest, Inventory, PurchaseRequestItem, Quotation, QuotationItem, Type

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

class RequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        exclude = ['requestedBy', 'requestLocation', 'dateApproved']

class RequestItemForm(forms.ModelForm):
    inventory = forms.ModelChoiceField(queryset=Inventory.objects.all(), required=True, empty_label="---------", to_field_name="id")

    class Meta:
        model = PurchaseRequestItem
        fields = ['inventory', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'required': True}),
        }
        
RequestItemFormSet = inlineformset_factory(PurchaseRequest, PurchaseRequestItem, form=RequestItemForm, extra=1, can_delete=False, can_delete_extra=True)

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        exclude = ['id', 'purchaseRequest', 'createdBy', 'dateCreated']

class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        exclude = ['id', 'quotation', 'approvedBy', 'dateApproved', 'deliverySet']
        widgets = {
            'inventory': forms.Select(attrs={'required': True}),
            'supplierName': forms.TextInput(attrs={'required': True}),
            'quantity': forms.NumberInput(attrs={'required': True}),
            'price': forms.NumberInput(attrs={'required': True}),
        }
        
QuotationItemFormSet = inlineformset_factory(Quotation, QuotationItem, form=QuotationItemForm, extra=1, can_delete=False, can_delete_extra=True)

# DELIVERY UPDATE FORMS
# class UpdateDateArrivedForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseRequest
#         fields = ['dateArrived']

#     def update_date_arrived(request, pk):
#         delivery = get_object_or_404(PurchaseRequest, pk=pk)
#         if request.method == 'POST':
#             form = UpdateDateArrivedForm(request.POST, instance=delivery)
#             if form.is_valid():
#                 delivery.update_dateArrived(form.cleaned_data['dateArrived'])
#                 return redirect('delivery_list')
#         else:
#             form = UpdateDateArrivedForm(instance=delivery)
#         return render(request, 'update_date_arrived.html', {'form': form})


# class UpdateDateApprovedForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseRequest
#         fields = ['dateApproved']

#     def update_date_approved(request, pk):
#         delivery = get_object_or_404(PurchaseRequest, pk=pk)
#         if request.method == 'POST':
#             form = UpdateDateApprovedForm(request.POST, instance=delivery)
#             if form.is_valid():
#                 delivery.update_dateApproved(form.cleaned_data['dateApproved'])
#                 return redirect('delivery_list')
#         else:
#             form = UpdateDateApprovedForm(instance=delivery)
#         return render(request, 'update_date_approved.html', {'form': form})

# ======================================================================================================== #