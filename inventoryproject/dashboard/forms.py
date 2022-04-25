from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Inventory
        fields = ['name', 'location', 'type', 'brand', 'status', 'quantity', 'remarks']
