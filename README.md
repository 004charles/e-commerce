# Marketplace Angola

Base independente do marketplace multi-loja, construída a partir do template `cidade da china.zip`.

## Regra visual principal

O ficheiro `src/templates/homepage/index.html` é a homepage oficial e deve ser tratado como um contrato visual e comportamental. A cópia em `reference/index.html` é a referência imutável usada para verificar alterações acidentais.

A assinatura atual da homepage integrada é igual à referência original. A estrutura, secções, carrosséis, modais, menus, footer e comportamentos JavaScript existentes foram preservados.

## Base implementada

A primeira fundação inclui Django, utilizador personalizado, lojas com estado de aprovação, categorias, produtos com stock e preços em `DecimalField`, homepage, catálogo com pesquisa e ordenação, detalhe de produto, perfil de loja aprovado e Django Admin.

A homepage já prepara contexto dinâmico para produtos em destaque, novidades, categorias e lojas aprovadas. A integração visual desses dados deve ser feita de forma aditiva, sem apagar ou reorganizar qualquer secção do `index.html`.

## Execução local

```bash
cd /home/ubuntu/workspace/marketplace-angola/src
python3 manage.py check
python3 manage.py migrate
python3 manage.py runserver 127.0.0.1:8000
```

Rotas iniciais:

| Rota | Função |
|---|---|
| `/` | Homepage baseada no `index.html` principal. |
| `/catalog/` | Catálogo com base em `shop-left-sidebar.html`. |
| `/catalog/category/<slug>/` | Catálogo filtrado por categoria. |
| `/catalog/product/<store-slug>/<slug>/` | Detalhe de produto. |
| `/stores/<slug>/` | Perfil público de loja aprovada. |
| `/admin/` | Administração de utilizadores, lojas, categorias e produtos. |

## Estrutura

```text
marketplace-angola/
├── README.md
├── reference/
│   ├── index.html
│   ├── index.sha256
│   └── assets/
├── src/
│   ├── accounts/
│   ├── catalog/
│   ├── homepage/
│   ├── stores/
│   ├── marketplace_config/
│   ├── templates/
│   ├── assets/
│   ├── manage.py
│   └── db.sqlite3
└── docs/
```

# e-commerce
