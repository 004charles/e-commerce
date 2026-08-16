# Auditoria da categoria Telemóveis — 2026-08-16

A página `/catalog/category/telemoveis/` estava sem estilo porque `list.html` usava 186 referências relativas `../assets/`. Numa URL aninhada, esses caminhos resolviam para `/catalog/assets/...` e falhavam. A substituição para `/assets/...` foi aplicada a CSS, fontes, imagens e JavaScript.

Após a correção, todos os seis CSS principais e o CSS de pesquisa responderam HTTP 200. O body tem `base-bg-color`, fundo calculado `rgb(242, 243, 248)`, e existem 69 cartões `productMain` com classes do Kartify.

A página ainda usa cartões HTML estáticos na grelha: não existe `{% for product %}` no template e os primeiros cartões têm nomes `Watch`, `Laptop`, `Marth product` e `Phone`. A correção de estilo já está validada; a integração dos produtos reais da categoria pode ser feita de forma aditiva no próximo ajuste, caso necessário.
