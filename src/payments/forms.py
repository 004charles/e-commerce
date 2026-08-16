from django import forms

from .models import PaymentAttempt


class PaymentMethodForm(forms.Form):
    method = forms.ChoiceField(
        label="Método de pagamento",
        choices=PaymentAttempt.Method.choices,
        widget=forms.RadioSelect,
    )
