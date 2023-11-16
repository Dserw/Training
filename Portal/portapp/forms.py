from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category', 'upload']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text_body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type comment text here ...'}),
        }
