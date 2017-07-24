from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.widgets import AdminFileWidget

from .models import *

class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class MemberForm(forms.ModelForm):
    goal_weight = forms.CharField(required=True)
    initial_weight = forms.CharField(required=True)
    class Meta:
        model = Members
        exclude = ['name']

class WeighinForm(forms.ModelForm):
    date = forms.DateField(required=True)
    weight = forms.CharField(max_length=5,required=True)
    photo = forms.FileField(required=True)

    class Meta:
        model = Weighins
        fields = ['member','date','weight','photo','left_arm','right_arm','left_leg','right_leg','waist','bum','chest']
