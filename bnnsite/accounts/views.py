#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from forms import LoginForm
from accounts.models import UserProfile



def set_lang(request):
    return render_to_response("set_lang.html", context_instance=RequestContext(request))


def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()    
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            if _login(request,form.cleaned_data["username"],form.cleaned_data["password"]):
                return HttpResponseRedirect(request.GET.get('next', reverse('index')))
    template_var["form"]=form
    return render_to_response("login.html",template_var,context_instance=RequestContext(request))
    
def _login(request,username,password):
    '''登陆核心方法'''
    ret=False
    user=authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))
    return ret
    
def logout(request):
    '''注销视图'''
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

