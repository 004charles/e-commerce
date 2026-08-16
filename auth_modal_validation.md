# Validação do modal de autenticação

O acesso a `/account/login/?next=/account/orders/` agora redireciona para `/?open_auth=1&next=%2Faccount%2Forders%2F`.

A homepage abre o modal original `authenticationModal` do template Kartify, com os campos de email e palavra-passe, botão de login, recuperação de palavra-passe e opção de criar conta. A página simples de login deixou de ser apresentada no fluxo de acesso às áreas protegidas.

Validações:

| Verificação | Resultado |
|---|---:|
| Redirecionamento de `/account/login/` | Homepage com `open_auth=1` |
| Modal original visível | Confirmado |
| Homepage carregada | HTTP 200 |
| Script de autenticação | Sintaxe válida |
| Suíte Django | 16 testes aprovados |
| Estrutura original da homepage | Preservada |
