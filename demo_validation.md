# Validação dos dados de demonstração

Data: 15 de agosto de 2026.

A homepage pública carregou com HTTP 200 e mostrou a secção dinâmica **Produtos publicados pelas lojas**. Foram confirmados produtos reais provenientes das três lojas de demonstração, com links de detalhe, imagem em `/media/catalog/products/demo/`, preço em Kz e stock disponível.

Produtos visualmente confirmados: Candeeiro LED Decorativo, Organizador Multiusos para Casa, Vestido Casual Elegante, T-shirt Premium Algodão, Auscultadores Bluetooth Premium, Smartphone Android Pro 128GB, Mochila Casual Resistente, Conjunto de Utensílios de Cozinha, Mala Feminina Clássica, Ténis Urban Street, Coluna Portátil Bluetooth e Relógio Inteligente Series X3.

Lojas confirmadas: Nova Era Casa & Acessórios, Novo São Paulo Fashion e Cidade da China Eletrónica.

A secção original Flash Sale, os menus, carrosséis e modais continuam visíveis; a secção de produtos reais foi acrescentada de forma dinâmica após a secção Flash Sale.

O endpoint `/home/data/` devolveu HTTP 200 com 12 produtos ativos, incluindo URLs absolutas de imagem e detalhe. O catálogo `/catalog/` devolveu HTTP 200 e mostrou os produtos reais na grelha adicional.

## Validação da correção do template

Após a correção, a pesquisa visual não encontrou a secção adicional **Produtos publicados pelas lojas**. Em contrapartida, o produto **Candeeiro LED Decorativo** apareceu dentro do carrossel original **Flash Sale**, com a imagem, nome, preço, loja e stock atualizados. A estrutura do cartão, o carrossel e as dimensões originais permanecem os mesmos; a integração apenas altera os dados internos dos cartões existentes.

Também foi confirmado no código que o catálogo já não contém o bloco `marketplace-live-catalog`, e que o script da homepage já não utiliza criação dinâmica de novos elementos ou inserção de uma nova secção.
