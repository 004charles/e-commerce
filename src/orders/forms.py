from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "province",
            "municipality",
            "address",
            "address_details",
            "notes",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel"}),
            "province": forms.TextInput(attrs={"class": "form-control", "autocomplete": "address-level1"}),
            "municipality": forms.TextInput(attrs={"class": "form-control", "autocomplete": "address-level2"}),
            "address": forms.TextInput(attrs={"class": "form-control", "autocomplete": "street-address"}),
            "address_details": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "customer_name": "Nome completo",
            "customer_email": "Email",
            "customer_phone": "Telefone",
            "province": "Província",
            "municipality": "Município",
            "address": "Morada de entrega",
            "address_details": "Complemento da morada",
            "notes": "Observações do pedido",
        }
        help_texts = {
            "address_details": "Ponto de referência, edifício ou andar, se necessário.",
            "notes": "Indicações adicionais para a entrega.",
        }
