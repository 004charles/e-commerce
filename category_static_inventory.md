# Inventário de dados estáticos da categoria

A página de categoria não possui qualquer loop `{% for product %}` no template `catalog/list.html`; os cartões são HTML estático do Kartify.

A página contém 69 cartões `.productMain` organizados em grupos: 7 no `menu-product-slider`, 48 no `menu-product-slider2` (incluindo o grupo que não está visível no viewport) e 14 cartões isolados em `product-box-4-main`, correspondentes à grelha principal e blocos de produtos.

Os primeiros cartões têm nomes de demonstração como `Watch`, `Laptop`, `Marth product`, `Phone`, `Beauty`, `Furniture`, `Perfume` e `Headphone`. A categoria Telemóveis deve receber produtos reais filtrados por `category_slug`, mantendo os cartões, o Swiper, as dimensões e as classes originais.

A solução deve alimentar, de forma aditiva, os cartões existentes, o cabeçalho, a pesquisa e os filtros com contexto do banco; não deve criar novas grelhas nem remover componentes do template.
