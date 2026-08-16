# Auditoria dos links da homepage

A auditoria DOM encontrou links ainda não limpos:

- Seletor de idioma: `Por`, `Eng`, `中`, `Esp`, `Fr`; estes são funcionais e devem permanecer traduzidos.
- Seletor de moeda: `AUD`, `EUR`, `CNY`; deve ser substituído por apenas `AOA`, pois a plataforma usa AOA como moeda padrão.
- Link de logótipo ainda aponta para `index.html`; deve apontar para `/`.
- Dropdown de pesquisa contém rótulos traduzidos, mas ainda aponta para `index.html#!`; deve apontar para `/catalog/` ou para categorias reais.
- `Limpar tudo` ainda aponta para `index.html#!`; deve executar a limpeza das pesquisas ou apontar para a pesquisa real.
- Ainda existe um segundo botão/modal de autenticação com `Log In`; deve ser traduzido para `Entrar` e usar `/?open_auth=1`.
- Existem links vazios ou demonstrativos no cabeçalho e menu mobile.
- O menu Home ainda contém demos como Gadget Store, MegaMart Store e Coming Soon.
- Os links do menu Shop/Product/Features/Pages ainda contêm páginas Kartify sem rota Django.
- Alguns itens de pesquisa populares ainda têm nomes comerciais em inglês, embora já apontem para `/catalog/`.

A lista completa foi extraída para `/home/ubuntu/console_outputs/exec_result_2026-08-16_06-46-01_136.txt`.
