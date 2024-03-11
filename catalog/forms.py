from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа',
                       'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        return self.clean_text(self.cleaned_data.get('name'), 'Такое название запрещено')

    def clean_description(self):
        return self.clean_text(self.cleaned_data.get('description'), 'Такое описание запрещено')

    def clean_text(self, text, error_message):
        for word in self.forbidden_words:
            if word.lower() in text.lower():
                raise forms.ValidationError(error_message)
        return text


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        exclude = ('product',)
