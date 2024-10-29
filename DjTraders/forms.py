from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'contact_name', 'address', 'city', 'postal_code', 'country', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_customer_name(self):
        name = self.cleaned_data['customer_name']
        if any(char.isdigit() for char in name):
            raise ValidationError("Customer name should not contain numbers.")
        if len(name.strip()) < 2:
            raise ValidationError("Customer name must be at least 2 characters long.")
        return name.strip()

    def clean_contact_name(self):
        name = self.cleaned_data['contact_name']
        if any(char.isdigit() for char in name):
            raise ValidationError("Contact name should not contain numbers.")
        if len(name.strip()) < 2:
            raise ValidationError("Contact name must be at least 2 characters long.")
        return name.strip()

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not any(char.isdigit() for char in postal_code):
            raise ValidationError("Postal code must contain at least one number.")
        return postal_code.strip()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'unit', 'price', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'})
        }

    def clean_product_name(self):
        name = self.cleaned_data['product_name']
        if any(char.isdigit() for char in name):
            raise ValidationError("Product name should not contain numbers.")
        if len(name.strip()) < 2:
            raise ValidationError("Product name must be at least 2 characters long.")
        return name.strip()

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        if price > 10000:
            raise ValidationError("Price cannot exceed $10,000.")
        return price

    def clean_unit(self):
        unit = self.cleaned_data['unit']
        if len(unit.strip()) < 1:
            raise ValidationError("Unit cannot be empty.")
        return unit.strip()

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validations here if needed
        return cleaned_data