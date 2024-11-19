from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Customer, Product, Category

# Custom validators
no_numbers_validator = RegexValidator(
    regex=r"^[^\d]+$", message="This field should not contain numbers."
)


class CustomerForm(forms.ModelForm):
    customer_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={"required": True}),
        label="Customer Name",
    )
    contact_name = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={"required": True}),
        label="Contact Name",
    )
    address = forms.CharField(
        min_length=3,
        error_messages={
            "required": "Address is required.",
            "min_length": "Address must be at least 3 characters long.",
        },
        widget=forms.TextInput(attrs={"required": True}),
        label="Address",
    )
    city = forms.CharField(
        validators=[no_numbers_validator],
        widget=forms.TextInput(attrs={"required": True}),
        label="City",
    )
    country = forms.ChoiceField(
        choices=[
            ("USA", "United States"),
            ("CAN", "Canada"),
            ("MEX", "Mexico"),
            ("GBR", "United Kingdom"),
            ("FRA", "France"),
            ("GER", "Germany"),
        ],
        label="Country",
    )
    postal_code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{5}(?:-\d{4})?$", message="Enter a valid postal code."
            )
        ],
        widget=forms.TextInput(attrs={"required": True}),
        label="Postal Code",
    )

    class Meta:
        model = Customer
        fields = [
            "customer_name",
            "contact_name",
            "address",
            "city",
            "postal_code",
            "country",
            "status",
        ]

    def clean_city(self):
        city = self.cleaned_data.get("city", "")
        if any(char.isdigit() for char in city):
            raise ValidationError("City should not contain numbers.")
        if len(city.strip()) < 2:
            raise ValidationError("City name must be at least 2 characters long.")
        return city.strip()

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code", "")
        if not postal_code.strip():
            raise ValidationError("Postal code is required.")
        if not any(char.isdigit() for char in postal_code):
            raise ValidationError("Postal code must contain at least one number.")
        if len(postal_code.strip()) < 5:
            raise ValidationError("Postal code must be at least 5 characters long.")
        return postal_code.strip()

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        country = cleaned_data.get("country")
        if city and country and city.lower() == country.lower():
            raise ValidationError("City and Country cannot be the same.")
        return cleaned_data


class ProductForm(forms.ModelForm):
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={"required": True}), label="Product Name"
    )
    price = forms.DecimalField(
        min_value=0,
        error_messages={
            "required": "Price is required.",
            "min_value": "Price must be a positive number.",
        },
        widget=forms.NumberInput(attrs={"required": True}),
        label="Price",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        to_field_name="category_id",
        label="Category",
    )

    class Meta:
        model = Product
        fields = ["product_name", "category", "unit", "price", "status"]

    def clean_product_name(self):
        product_name = self.cleaned_data.get("product_name", "")
        if not product_name.strip():
            raise ValidationError("Product name is required.")
        return product_name.strip()

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price
