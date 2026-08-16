import os
import sys

sys.path.insert(0, "/home/ubuntu/workspace/marketplace-angola/src")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace_config.settings")
import django

django.setup()

from accounts.models import User

for username in ["demo-cidade-china", "demo-novo-sao-paulo", "demo-nova-era", "cliente-demo"]:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"{username}: MISSING")
        continue
    expected = "DemoAngola2026!" if username != "cliente-demo" else "ClienteDemo2026!"
    print(f"{username}: email={user.email} role={user.role} active={user.is_active} password_ok={user.check_password(expected)}")
