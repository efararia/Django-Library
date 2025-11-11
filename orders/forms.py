from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book_title', 'note']
        widgets = {
            'book_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کتاب مورد نظر'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات (اختیاری)', 'rows': 3}),
        }
