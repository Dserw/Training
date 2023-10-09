from django import forms
from .models import Post


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['head', 'text', 'author', 'category', ]
        widgets = {
            'type': forms.HiddenInput(),
            'category': forms.CheckboxSelectMultiple,
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['head', 'text', 'author', 'category', ]
        widgets = {
            'type': forms.HiddenInput(),
            'category': forms.CheckboxSelectMultiple,
        }
