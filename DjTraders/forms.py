from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .models import Customer, Product

# Validator to ensure fields do not contain numbers
no_numbers_validator = RegexValidator(
    regex=r'^[^\d]+$',
    message="This field should not contain numbers."
)

class CustomerForm(forms.ModelForm):
    # Apply the no_numbers_validator to relevant fields
    customer_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )
    contact_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )
    city = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )
    country = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )

    # Postal code validator (assuming US ZIP code format)
    postal_code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{5}(?:-\d{4})?$',
                message="Enter a valid postal code."
            )
        ],
        widget=forms.TextInput(attrs={'required': True})
    )

    class Meta:
        model = Customer
        fields = ['customer_name', 'contact_name', 'address', 'city', 'postal_code', 'country', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if len(address) < 5:
            raise ValidationError("Address must be at least 5 characters long.")
        return address

    def clean(self):
        cleaned_data = super().clean()
        # Example of cross-field validation if needed
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')
        if city and country and city.lower() == country.lower():
            raise ValidationError("City and Country cannot be the same.")
        return cleaned_data

class ProductForm(forms.ModelForm):
    # Apply the no_numbers_validator to product_name and unit
    product_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )
    unit = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True})
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="Price must be greater than zero."),
            MaxValueValidator(10000, message="Price cannot exceed $10,000.")
        ],
        widget=forms.NumberInput(attrs={'required': True, 'min': '0.01', 'step': '0.01'})
    )

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'unit', 'price', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validations here if needed
        return cleaned_data

class CustomerForm(forms.ModelForm):
    COUNTRY_CHOICES = [
        ('USA', 'United States'),
        ('CAN', 'Canada'),
        ('MEX', 'Mexico'),
        ('GBR', 'United Kingdom'),
        ('FRA', 'France'),
        ('GER', 'Germany'),
        # Add other countries as needed
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    class Meta:
        model = Customer
        fields = ['customer_name', 'contact_name', 'address', 'city', 'postal_code', 'country', 'status']