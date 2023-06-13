from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
    postContent = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':4, 'style':'resize: None'}
            ),
        max_length=200, label="Post content")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-newPost'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'createpost'

        self.helper.add_input(Submit('create post','Create-Post',))


    class Meta:
        model = Post
        fields = [ "postContent"]