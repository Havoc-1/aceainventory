from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import *

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
        exclude = ['requestedBy', 'requestLocation', 'dateRequested', 'dateApproved', 'approvedQuotations', 'approvedDelivery', 'confirmedDeliveryCount', 'totalDeliveryCount']

class RequestItemForm(forms.ModelForm):
    inventory = forms.ModelChoiceField(queryset=Inventory.objects.all(), required=True, empty_label="---------", to_field_name="id")

    class Meta:
        model = PurchaseRequestItem
        fields = ['inventory', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'required': True}),
        }
        

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

class PartialDeliveryForm(forms.ModelForm):
    expectedDeliveryDate = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y'), 
                               attrs={'required': True}))
    class Meta:
        model = DeliveryItem
        exclude = ['id', 'quotationItem', 'quantity', 'inventory', 'deliveryLocation', 'approvedBy', 'dateApproved', 'dateArrived']
        widgets = {
            'pQuantity': forms.NumberInput(attrs={'required': True}),
        }

PartialDeliveryFormSet = forms.formset_factory(PartialDeliveryForm, extra=1)

class InventoryWithdrawnForm(forms.ModelForm):
    class Meta:
        model = InventoryWithdrawn
        fields = ['inventory', 'quantity']
        widgets = {
            'inventory': forms.Select(attrs={'required': True}),
            'quantity': forms.NumberInput(attrs={'required': True}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inventory'].queryset = Inventory.objects.filter(quantity__gt=0)
        
InventoryWithdrawnFormSet = modelformset_factory(
    InventoryWithdrawn, form=InventoryWithdrawnForm, extra=1)

class InventoryReturnedForm(forms.ModelForm):
    class Meta:
        model = InventoryReturned
        fields = ['inventory', 'quantity', 'transferredTo']
        exclude = ['transferredFrom']
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'transferredTo': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

InventoryReturnedFormSet = forms.modelformset_factory(
    InventoryReturned,
    form=InventoryReturnedForm,
    extra=1,
    can_delete=True
)

class InventoryDamagedForm(forms.ModelForm):
    class Meta:
        model = InventoryDamaged
        fields = ['inventory', 'quantity', 'remarks']
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')