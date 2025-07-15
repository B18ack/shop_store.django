from django import forms
from django.core.exceptions import ValidationError

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, max_quantity=10, available_quantity=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_quantity = available_quantity
        self.fields['quantity'].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.available_quantity:
            raise ValidationError(f"Недостаточно товара на складе. Доступно только {self.available_quantity}.")
        return quantity