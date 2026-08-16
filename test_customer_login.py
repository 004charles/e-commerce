import os
import sys

sys.path.insert(0, "/home/ubuntu/workspace/marketplace-angola/src")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace_config.settings")
import django

django.setup()

from django.test import Client

client = Client(HTTP_HOST="127.0.0.1")
response = client.post(
    "/account/modal/login/",
    {"email": "cliente.demo@marketplace.test", "password": "ClienteDemo2026!"},
)
print("status=" + str(response.status_code))
print(response.json())
