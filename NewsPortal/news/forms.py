from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    headline = forms.CharField(min_length=5, label='Заголовок')
    body = forms.CharField(widget=forms.Textarea, label='Текст')

    class Meta:
        model = Post
        fields = ['headline', 'body', 'categories', 'author']

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        body = cleaned_data.get("body")

        if headline and body and headline == body:
            raise ValidationError(
                "Заголовок и текст не должны быть идентичны."
            )

        return cleaned_data