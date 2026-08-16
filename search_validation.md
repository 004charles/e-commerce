# Validação da pesquisa multi-loja

A barra original da homepage recebeu a consulta `smartphone` sem alterar a sua estrutura. O bloco original de resultados mostrou o produto real `Smartphone Android Pro 128GB`, a loja `Cidade da China Eletrónica`, a localização `Viana, Luanda`, o preço `185 000,00 Kz`, o preço anterior `210 000,00 Kz` e a indicação `Menor preço`.

Os resultados são obtidos por AJAX através de `/home/search/?q=smartphone`. O endpoint filtra produtos ativos, com stock disponível e lojas aprovadas, pesquisando por nome, descrição, categoria, loja, província e município.

A pesquisa também pode ser submetida com Enter ou pelo botão original, levando para `/catalog/?q=...`.

## Teste solicitado: tenis e laptop

O termo `tenis` foi testado no endpoint e diretamente na barra original. A normalização de acentos encontrou corretamente `Ténis Urban Street`, da loja `Novo São Paulo Fashion`, localizada em `Cazenga, Luanda`, com preço `45 000,00 Kz` e preço anterior `55 000,00 Kz`. A barra exibiu o resultado com a indicação `Menor Preço`.

O termo `laptop` também foi testado no endpoint e na barra original. O resultado correto foi zero, porque não existe atualmente nenhum produto real cadastrado com “laptop” no nome, descrição, categoria ou loja. A interface exibiu `Nenhum produto encontrado.` sem apresentar dados demo incorretos.

## Comparação multi-loja

Foi adicionada uma segunda oferta real de `Ténis Urban Street` para demonstrar comparação entre vendedores. A pesquisa `tenis` devolve duas ofertas e uma comparação:

| Loja | Localização | Preço | Menor preço |
|---|---|---:|---:|
| Cidade da China Eletrónica | Viana, Luanda | 42.000,00 Kz | Sim |
| Novo São Paulo Fashion | Cazenga, Luanda | 45.000,00 Kz | Não |

A indicação `Comparar preços: 2 lojas` foi adicionada ao resultado usando o mesmo bloco original da barra de pesquisa. Os filtros de província, loja, preço mínimo e preço máximo também foram validados no endpoint e no catálogo.
