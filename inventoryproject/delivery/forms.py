from django import forms
from .models import Inventory, Delivery, DeliveryItem   
from django.forms import ModelChoiceField                    

# NOT YET IMPLEMENTED

class DeliveryRequestForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Delivery
        fields = ['inventory', 'staff', 'status', 'remarks']

    inventory = forms.ModelMultipleChoiceField(
        queryset=DeliveryItem.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class DeliveryRequestItemForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = DeliveryItem
        fields = ['name', 'quantity', 'specifications']