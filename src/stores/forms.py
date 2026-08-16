from django import forms

from orders.models import Order

from .models import StoreApplication


class StoreOrderStatusForm(forms.Form):
    status = forms.ChoiceField(
        label="Estado do pedido",
        choices=[
            (Order.Status.AWAITING_PAYMENT, "A aguardar pagamento"),
            (Order.Status.PAID, "Pago"),
            (Order.Status.PROCESSING, "Em preparação"),
            (Order.Status.SHIPPED, "Enviado"),
            (Order.Status.COMPLETED, "Concluído"),
            (Order.Status.CANCELLED, "Cancelado"),
        ],
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )


class StoreApplicationForm(forms.ModelForm):
    class Meta:
        model = StoreApplication
        fields = (
            "proposed_name",
            "description",
            "phone",
            "whatsapp",
            "province",
            "municipality",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
