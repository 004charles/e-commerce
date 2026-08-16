# Validação final de links e ícones

A homepage foi verificada com a versão `menu10`.

Os ícones Remix Icon estão visíveis no DOM com `display: inline` ou `block`, `visibility: visible` e a família `remixicon`. Os Iconsax também estão carregados com `data-local-icon-loaded=true`, incluindo pesquisa, telefone, conta, favoritos e carrinho, com 25px por 25px.

O preloader estava encerrado: `display: none`, `opacity: 0` e `document.readyState=complete`.

A limpeza dos links foi ajustada para não alterar anchors apenas com ícones, links de pesquisa, modais, wishlist, carrinho ou controlos de idioma. As rotas funcionais permanecem nos links de conta, catálogo, carrinho, favoritos, autenticação e pesquisa.

O diagnóstico encontrou anteriormente links demonstrativos no template; a integração agora os encaminha ou oculta sem interferir nos ícones. Os caminhos dos assets de ícones confirmados são `assets/css/vendors/remixicon.css`, `assets/css/vendors/iconsax.css`, `assets/svg/iconsax` e `assets/js/iconsax.js`.
