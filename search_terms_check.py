import json
import sys

payload = json.load(sys.stdin)
print(f"count={payload['count']}")
for result in payload["results"]:
    print(
        f"{result['name']} | loja={result['store']} | "
        f"localizacao={result['location']} | preco={result['price']} Kz | "
        f"anterior={result['compare_at_price'] or '-'}"
    )
