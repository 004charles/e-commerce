from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Cliente"
        STORE_OWNER = "store_owner", "Proprietário de loja"
        STAFF = "staff", "Funcionário"
        ADMIN = "admin", "Administrador"

    email = models.EmailField("email", unique=True)
    phone = models.CharField("telefone", max_length=30, blank=True)
    role = models.CharField(
        "perfil",
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    def __str__(self):
        return self.get_full_name() or self.username
