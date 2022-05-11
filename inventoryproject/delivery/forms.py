from django import forms
from .models import Inventory, Delivery                         

# NOT YET IMPLEMENTED

class DeliveryRequestForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Delivery
        fields = ['inventory', 'quantity']

    quantity = forms.IntegerField()
    inventory = forms.ModelMultipleChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
