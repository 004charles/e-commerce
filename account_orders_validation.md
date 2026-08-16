# Validação da área de conta do cliente

Foi criada a área de conta com perfil, lista de pedidos e detalhe de pedido.

Rotas protegidas:

- `/account/profile/`
- `/account/orders/`
- `/account/orders/<order_number>/`

Um cliente autenticado consulta apenas pedidos cujo campo `user` corresponde ao próprio utilizador. O detalhe utiliza `get_object_or_404` com esse filtro, impedindo que um cliente abra o pedido de outra conta.

Validações concluídas:

| Verificação | Resultado |
|---|---:|
| `manage.py check` | Sem erros |
| Suíte Django | 16 testes aprovados |
| Lista de pedidos do cliente | Aprovada |
| Detalhe do próprio pedido | Aprovado |
| Acesso ao pedido de outro cliente | HTTP 404 |
| `/account/profile/` sem login | HTTP 302 para login |
| `/account/orders/` sem login | HTTP 302 para login |
| Lojas, estados, totais e linhas | Apresentados |
