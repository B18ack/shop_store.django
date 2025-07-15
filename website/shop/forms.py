from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from . import models

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        errors = []
    

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',  'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            )
            ,
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['title', 'preview','description', 'category', 'price', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            "preview": forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    website = forms.URLField(required=False)
    message = forms.CharField(widget=forms.Textarea)