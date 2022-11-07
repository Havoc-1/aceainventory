from django import forms
from .models import Inventory, Type

class InventoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Inventory
        fields = ['name', 'location', 'type', 'brand', 'status', 'quantity', 'remarks']

class CategoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Type
        fields = ['name',]
