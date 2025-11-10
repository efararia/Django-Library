from django import forms
from .models import BookRating

class BookRatingForm(forms.ModelForm):
    RATING_CHOICES = [
        ('1', '1 ستاره'),
        ('2', '2 ستاره'),
        ('3', '3 ستاره'),
        ('4', '4 ستاره'),
        ('5', '5 ستاره'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'rating-select'}),
        label='رتبه‌بندی'
    )
    
    class Meta:
        model = BookRating
        fields = ['rating']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.rating = int(self.cleaned_data['rating'])
        if commit:
            instance.save()
        return instance

