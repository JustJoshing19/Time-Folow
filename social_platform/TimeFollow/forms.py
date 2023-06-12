from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class NewPost(forms.ModelForm):
    postContent = forms.CharField(widget=forms.Textarea(
        attrs={'rows':4, 'style':'resize: None'}
        ),
        max_length=200)
    class Meta:
        model = Post
        fields = [ "postContent"]