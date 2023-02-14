from django import forms
from django.forms import inlineformset_factory
from .models import Delivery, Product, DeliveryItem, Type

class ProductForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        abstract = True
        model = Product
        fields = ['name', 'location', 'type', 'quantity',]
        
class CategoryForm(forms.ModelForm):
    class Meta:         # meta takes at least 2 parameters
        model = Type
        fields = ['name',]

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_location',]

class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = '__all__'
        
DeliveryItemFormSet = inlineformset_factory(Delivery, DeliveryItem, form=DeliveryItemForm, extra=1)