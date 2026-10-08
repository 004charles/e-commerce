from django.contrib import admin

from .models import PaymentAttempt, PaymentProviderConfig


admin.site.register(PaymentProviderConfig)
admin.site.register(PaymentAttempt)
