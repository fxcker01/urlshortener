from django import forms
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com',
                'style': 'width: 100%; padding: 0.5rem; font-size: 1rem; border-radius: 6px;'
            }),
            'short_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Custom short code (optional)',
                'style': 'width: 100%; padding: 0.5rem; font-size: 1rem; border-radius: 6px;'
            }),
        }

