from django import forms
from .models import Sale, Purchase

from django import forms
from .models import Sale, Purchase

class SaleForm(forms.ModelForm):
    selling_price = forms.DecimalField(label='Selling Price', required=True)
    
    class Meta:
        model = Sale
        fields = ['quantity', 'tax', 'selling_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selling_price'].widget.attrs.update({'class': 'form-control'})

class PurchaseForm(forms.ModelForm):
    purchase_price = forms.DecimalField(label='Purchase Price', required=True)
    
    class Meta:
        model = Purchase
        fields = ['quantity', 'tax', 'purchase_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_price'].widget.attrs.update({'class': 'form-control'})

