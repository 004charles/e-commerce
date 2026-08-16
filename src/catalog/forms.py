from django import forms
from django.utils.text import slugify

from .models import Product, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[
                    (5, "5 estrelas"),
                    (4, "4 estrelas"),
                    (3, "3 estrelas"),
                    (2, "2 estrelas"),
                    (1, "1 estrela"),
                ],
                attrs={"class": "form-select"},
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Escreve o teu comentário",
                }
            ),
        }
        labels = {"rating": "Classificação", "comment": "Comentário"}

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating not in range(1, 6):
            raise forms.ValidationError("A classificação deve estar entre 1 e 5 estrelas.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()
        if len(comment) < 3:
            raise forms.ValidationError("O comentário deve ter pelo menos 3 caracteres.")
        return comment


class ProductForm(forms.ModelForm):
    def __init__(self, *args, store=None, **kwargs):
        self.store = store
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()
        for name in ("featured", "is_new"):
            self.fields[name].widget.attrs["class"] = "form-check-input"
        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "sku",
            "short_description",
            "description",
            "image",
            "price",
            "compare_at_price",
            "stock",
            "status",
            "featured",
            "is_new",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "short_description": forms.Textarea(attrs={"rows": 2}),
            "price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "compare_at_price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"min": "0", "step": "1"}),
        }

    def clean_sku(self):
        sku = self.cleaned_data["sku"].strip()
        if self.store is not None:
            queryset = Product.objects.filter(store=self.store, sku=sku)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("Já existe um produto com este SKU na sua loja.")
        return sku

    def clean_slug(self):
        slug = self.cleaned_data.get("slug") or slugify(self.cleaned_data.get("name", ""))
        if not slug:
            raise forms.ValidationError("Indique um nome válido para gerar o slug.")
        if self.store is not None:
            queryset = Product.objects.filter(store=self.store, slug=slug)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("Já existe um produto com este slug na sua loja.")
        return slug

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("O preço deve ser superior a zero.")
        return price

    def clean_compare_at_price(self):
        compare_at_price = self.cleaned_data.get("compare_at_price")
        price = self.cleaned_data.get("price")
        if compare_at_price is not None and price is not None and compare_at_price < price:
            raise forms.ValidationError("O preço anterior deve ser igual ou superior ao preço atual.")
        return compare_at_price

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock")
        status = cleaned_data.get("status")
        if stock is not None and stock == 0 and status == Product.Status.ACTIVE:
            self.add_error("status", "Um produto sem stock não pode ser publicado como ativo.")
        return cleaned_data
