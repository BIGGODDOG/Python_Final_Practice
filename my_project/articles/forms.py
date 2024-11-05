from django import forms
from .models import Article, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'restricted', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'tags': forms.TextInput(attrs={'placeholder': 'Введите теги, разделенные запятыми'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'] 
        if commit:
            user.save()
        return user