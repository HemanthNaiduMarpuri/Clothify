from django import forms
from products.models import Product, Category, Brand

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category':forms.Select(attrs={'class':'form-select'}),
            'brand':forms.Select(attrs={'class':'form-select'}),
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'product_slug':forms.TextInput(attrs={'class':'form-control'}),
            'product_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'product_description':forms.Textarea(attrs={'class':'form-control', 'rows':4}),
            'product_price':forms.NumberInput(attrs={'class':'form-control'}),
            'original_price':forms.NumberInput(attrs={'class':'form-control'}),
            'discounted_price':forms.NumberInput(attrs={'class':'form-control'}),
            'has_discounted':forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        has_discounted = cleaned_data.get('has_discounted')
        original_price = cleaned_data.get('original_price')
        discounted_price = cleaned_data.get('discounted_price')

        if has_discounted:
            if  original_price is None or discounted_price is None:
                raise ValueError("Discounted Products must have prices")
            elif discounted_price >= original_price:
                raise ValueError("Discounted prices should be less")
        else:
            original_price = None
            discounted_price = None
        
        return cleaned_data
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category_name':forms.TextInput(attrs={'class':'form-control'}),
            'category_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'category_slug':forms.TextInput(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['category_slug'].widget.attrs['readonly'] = True
            

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'brand_name':forms.TextInput(attrs={'class':'form-control'}),
            'brand_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'brand_slug':forms.TextInput(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['brand_slug'].widget.attrs['readonly'] = True