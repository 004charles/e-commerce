# Auditoria da homepage — 2026-08-16

A homepage pública carrega corretamente os scripts aditivos e já atualiza categorias, contactos principais e os cartões `.product-box.productMain` visíveis. O primeiro cartão dinâmico observado no DOM é **Auscultadores Bluetooth Premium**.

O problema restante está nos cartões `.vertical-product-box` dentro das secções da homepage: a primeira recomendação ainda mostra **Apple iPhone 14**, **BlackBerry Keyone**, **Refurb Macbook** e preços em USD. Foram identificados 62 cartões `productMain`, 35 cartões verticais dentro de `section` e 47 cartões verticais no total, contando também carrinho/wishlist.

O endpoint `/home/data/` devolve atualmente 24 produtos, o que deixa cartões posteriores com conteúdo estático. A correção deve devolver produtos suficientes para todos os cartões principais, aplicar os dados também a `section .vertical-product-box`, e atualizar nome, URL, imagem, preço e preço anterior usando AOA/Kz.

Os títulos ainda estáticos observados incluem `Flash Sale`, `Get it all right here`, `Recommendations`, `Hot Tag:` e `Don't Miss This Offers`. A morada do rodapé ainda mostra `3228 Bicetown Road Huntington, NY 11743`; o script atual atualiza telefone/email, mas não a morada.

Restrição confirmada: não alterar a estrutura do `index.html`; a correção será feita nos endpoints, no seed de conteúdo e nos scripts aditivos.
