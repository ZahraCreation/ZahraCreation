from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            "customer_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "payment_method",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Your full name",
                    "class": "checkout-input",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "your@email.com",
                    "class": "checkout-input",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "10-digit mobile number",
                    "class": "checkout-input",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "placeholder": "House number, street, area",
                    "class": "checkout-input",
                    "rows": 4,
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "City",
                    "class": "checkout-input",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "placeholder": "State",
                    "class": "checkout-input",
                }
            ),
            "pincode": forms.TextInput(
                attrs={
                    "placeholder": "PIN code",
                    "class": "checkout-input",
                }
            ),
            "payment_method": forms.Select(
                attrs={
                    "class": "checkout-input",
                }
            ),
        }