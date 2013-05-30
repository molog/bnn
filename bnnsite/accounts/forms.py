#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

    
class LoginForm(forms.Form):
    username=forms.CharField(label=_(u"Username"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"Password"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    