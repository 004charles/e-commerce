# Validação da homepage orientada por dados

A homepage pública foi aberta em 16 de agosto de 2026 no endereço com `?v=20260816site4`.

A verificação confirmou que o cabeçalho recebeu links vindos de `HomepageLink`, o contacto foi atualizado para `+244 923 000 000`, os banners passaram a usar imagens em `/media/homepage/banners/` e URLs `/catalog/`, e os cartões de produtos mostraram nomes do conteúdo configurado pelo endpoint `/home/data/`.

O carrossel de categorias também passou a apresentar categorias reais como `Acessórios`, `Casa e Cozinha`, `Eletrónica` e `Moda e Vestuário`.

O endpoint devolveu 13 produtos, 4 categorias e 16 banners. O endpoint `/home/site-data/` devolveu 2 blocos de texto e 10 links configuráveis.

A suite Django passou com 34 testes e os scripts `marketplace-home-data.js` e `marketplace-site-data.js` passaram na validação de sintaxe.
