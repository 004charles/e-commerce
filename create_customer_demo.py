import os
import sys

sys.path.insert(0, "/home/ubuntu/workspace/marketplace-angola/src")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace_config.settings")
import django

django.setup()

from accounts.models import User

user, created = User.objects.get_or_create(
    username="cliente-demo",
    defaults={
        "email": "cliente.demo@marketplace.test",
        "first_name": "Cliente",
        "last_name": "Demo",
        "role": User.Role.CUSTOMER,
        "is_active": True,
    },
)
user.email = "cliente.demo@marketplace.test"
user.first_name = "Cliente"
user.last_name = "Demo"
user.role = User.Role.CUSTOMER
user.is_active = True
user.set_password("ClienteDemo2026!")
user.save()
print("created=" + str(created))
print("username=cliente-demo")
print("email=cliente.demo@marketplace.test")
print("password=ClienteDemo2026!")
print("password_ok=" + str(user.check_password("ClienteDemo2026!")))
