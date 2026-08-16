# Validação inicial do carrinho

A homepage carregou os produtos reais dentro dos cartões originais do Flash Sale e o contador do carrinho iniciou em 0. Durante o teste, o link de texto original `cart.html` revelou uma rota 404 porque o Django ainda não tinha uma página legada correspondente. A correção será feita com um redirecionamento aditivo de `cart.html` para a homepage com abertura automática do offcanvas original, sem alterar o markup visual.

## Validação da rota legada e do offcanvas

A rota original `/cart.html` foi corrigida com HTTP 302 para `/?open_cart=1`. No navegador, a URL final carregou a homepage e a inspeção confirmou `#cartOffcanvas.show = true`; o offcanvas original abriu corretamente e o contador mostrou 0 quando o carrinho estava vazio.

A estrutura visual do offcanvas foi mantida. A implementação apenas substitui os itens demo por dados reais quando existem itens no carrinho.
