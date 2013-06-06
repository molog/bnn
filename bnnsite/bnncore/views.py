import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Sum

from models import PaymentSlip
from forms import PaymentSlipForm, BnnProfileForm


@login_required
def summary(request):
    """ calculate the previous 2 weeks summary and any outstanding notifications"""
    house = request.user.bnnprofile.house
    house_payments_qs = PaymentSlip.objects.filter(profile__house=house)
    
    today = datetime.date.today()
    week_day = today.weekday()
    this_week_slips = house_payments_qs.filter(paid_date__gte=today - datetime.timedelta(days=week_day))
    last_week_slips = house_payments_qs.filter(paid_date__gte=today - datetime.timedelta(days=week_day+7)).filter(paid_date__lt=today - datetime.timedelta(days=week_day))
    
    this_week_user_sums = this_week_slips.values('profile__nick_name').annotate(sum=Sum('total_amount'))
    last_week_user_sums = last_week_slips.values('profile__nick_name').annotate(sum=Sum('total_amount'))
    
    this_week_sum = sum([slip.total_amount for slip in this_week_slips])
    last_week_sum = sum([slip.total_amount for slip in last_week_slips])
    return render(request, 'summary.html', {'this_week_slips':this_week_slips, 
                                            'last_week_slips':last_week_slips,
                                            'this_week_user_sums':this_week_user_sums,
                                            'last_week_user_sums':last_week_user_sums,
                                            'this_week_sum':this_week_sum,
                                            'last_week_sum':last_week_sum})


@login_required
def add_slip(request):
    if request.method == 'POST':
        form = PaymentSlipForm(request.POST)
        if form.is_valid():
            slip = form.save(commit=False)
            slip.profile = request.user.bnnprofile
            slip.save()
            messages.add_message(request, messages.SUCCESS, 'Payment slip successfully added')
            return HttpResponseRedirect(reverse('summary'))
        else:
            messages.add_message(request, messages.ERROR, 'Please enter valid data.')

    else:
        form = PaymentSlipForm()
    return render(request, 'add_slip.html', {'form': form})


@login_required
def history(request):
    slips = PaymentSlip.objects.all()
    return render(request, 'history.html', {'slips':slips})
    


def edit_profile(request):
    profile = request.user.bnnprofile
    if request.method == 'POST':
        form = BnnProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile successfully updated.')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BnnProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form':form})