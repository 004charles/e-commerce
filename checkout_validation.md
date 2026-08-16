# Validação do checkout multi-loja

Foi criada a aplicação `orders` com os modelos `Order`, `StoreOrder` e `OrderItem`. O checkout aceita produtos de várias lojas no mesmo carrinho e cria um pedido principal com uma linha de pedido separada por loja.

O serviço de checkout usa uma transação, bloqueia os produtos para nova validação, confirma que a loja está aprovada, confirma que o produto está ativo e verifica novamente o stock. O preço é lido do produto no servidor e guardado em `unit_price` e `line_total`; o frontend não define o preço final.

O pedido inicial é criado com estado `A aguardar pagamento` e pagamento `Não iniciado`. Não foi adicionada nenhuma integração de pagamento fictícia. A camada está preparada para futuras integrações oficiais de Multicaixa Express, Unitel Money e PayPay.

Testes concluídos:

| Verificação | Resultado |
|---|---:|
| `manage.py check` | Sem erros |
| Suíte Django | 13 testes aprovados |
| Pedido com duas lojas | Aprovado |
| Pedido principal e dois pedidos de loja | Aprovado |
| Snapshots de preço e produto | Aprovado |
| Redução de stock após pedido | Aprovada |
| Bloqueio de quantidade acima do stock | Aprovado |
| Carrinho limpo após criação do pedido | Aprovado |
| Checkout vazio | Redireciona para a homepage |
| Rota `/orders/checkout/` | Ativa |
| CSS principal | HTTP 200 |
| JavaScript do carrinho | Sintaxe válida |

O botão original `Check Out` do offcanvas continua visualmente intacto e é redirecionado por uma integração JavaScript aditiva para `/orders/checkout/`.
