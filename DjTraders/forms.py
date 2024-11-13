from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Customer, Product

# Custom validators
no_numbers_validator = RegexValidator(
    regex=r'^[^\d]+$',
    message="This field should not contain numbers."
)

class CustomerForm(forms.ModelForm):
    """
    Form for creating and updating Customer records.
    Includes validation for names, address, and location information.
    """
    
    # Personal Information Fields
    customer_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True}),
        label="Customer Name"
    )
    contact_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True}),
        label="Contact Name"
    )
    
    # Location Fields
    address = forms.CharField(
        min_length=3,
        error_messages={
            'required': 'Address is required.',
            'min_length': 'Address must be at least 3 characters long.'
        },
        widget=forms.TextInput(attrs={'required': True}),
        label="Address"
    )
    city = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={'required': True}),
        label="City"
    )
    country = forms.ChoiceField(
        choices=[
            ('USA', 'United States'),
            ('CAN', 'Canada'),
            ('MEX', 'Mexico'),
            ('GBR', 'United Kingdom'),
            ('FRA', 'France'),
            ('GER', 'Germany'),
        ],
        label="Country"
    )
    postal_code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{5}(?:-\d{4})?$',
                message="Enter a valid postal code."
            )
        ],
        widget=forms.TextInput(attrs={'required': True}),
        label="Postal Code"
    )

    class Meta:
        model = Customer
        fields = ['customer_name', 'contact_name', 'address', 'city', 'postal_code', 'country', 'status']

    # Field-level validation methods
    def clean_city(self):
        """
        Validates city name:
        - Must not contain numbers
        - Must be at least 2 characters long
        """
        city = self.cleaned_data.get('city', '')
        if any(char.isdigit() for char in city):
            raise ValidationError("City should not contain numbers.")
        if len(city.strip()) < 2:
            raise ValidationError("City name must be at least 2 characters long.")
        return city.strip()

    def clean_postal_code(self):
        """
        Validates postal code:
        - Must not be empty
        - Must contain at least one number
        - Must be at least 5 characters long
        """
        postal_code = self.cleaned_data.get('postal_code', '')
        if not postal_code.strip():
            raise ValidationError("Postal code is required.")
        if not any(char.isdigit() for char in postal_code):
            raise ValidationError("Postal code must contain at least one number.")
        if len(postal_code.strip()) < 5:
            raise ValidationError("Postal code must be at least 5 characters long.")
        return postal_code.strip()

    def clean(self):
        """
        Form-level validation:
        - City and Country cannot be the same
        """
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')
        if city and country and city.lower() == country.lower():
            raise ValidationError("City and Country cannot be the same.")
        return cleaned_data


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product records.
    Includes validation for product details and pricing.
    """
    
    # Product Information Fields
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}),
        label="Product Name"
    )
    price = forms.DecimalField(
        min_value=0,
        error_messages={
            'required': 'Price is required.',
            'min_value': 'Price must be a positive number.'
        },
        widget=forms.NumberInput(attrs={'required': True}),
        label="Price"
    )
    category = forms.ChoiceField(
        choices=[
            ('ELECTRONICS', 'Electronics'),
            ('FURNITURE', 'Furniture'),
            ('CLOTHING', 'Clothing'),
            # Add more categories as needed
        ],
        label="Category"
    )

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'unit', 'price', 'status']

    # Field-level validation methods
    def clean_product_name(self):
        """
        Validates product name:
        - Must not be empty
        """
        product_name = self.cleaned_data.get('product_name', '')
        if not product_name.strip():
            raise ValidationError("Product name is required.")
        return product_name.strip()

    def clean_price(self):
        """
        Validates price:
        - Must be greater than zero
        """
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price