import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Sum, Q

from models import PaymentSlip
from forms import PaymentSlipForm, BnnProfileForm, HouseForm


@login_required
def summary(request):
    """ calculate the previous 2 weeks summary and any outstanding notifications"""
    house = request.user.bnnprofile.house
   
    this_week_slips = get_week_slips(house=house)
    last_week_slips = get_week_slips(week=1, house=house)
    
    this_week_user_sums = this_week_slips.values('profile__nick_name').annotate(sum=Sum('total_amount'))
    last_week_user_sums = last_week_slips.values('profile__nick_name').annotate(sum=Sum('total_amount'))
    
    this_week_sum = this_week_slips.aggregate(sum=Sum('total_amount'))['sum']
    last_week_sum = last_week_slips.aggregate(sum=Sum('total_amount'))['sum']
    return render(request, 'summary.html', {'this_week_slips':this_week_slips, 
                                            'last_week_slips':last_week_slips,
                                            'this_week_user_sums':this_week_user_sums,
                                            'last_week_user_sums':last_week_user_sums,
                                            'this_week_sum':this_week_sum,
                                            'last_week_sum':last_week_sum})

def get_week_slips(week=0, user=None, house=None):
    """ get all payment slips for a given week. current week is 0, last week is 1 and so on """
    today = datetime.date.today()
    week_day = today.weekday()
    queries = Q()
    if user:
        queries &= Q(profile=user.bnnprofile)
    elif house:
        queries &= Q(profile__house=house)
    return PaymentSlip.objects.filter(queries).filter(paid_date__gte=today - datetime.timedelta(days=week_day+7*week)).filter(paid_date__lt=today - datetime.timedelta(days=week_day+7*(week-1)))


@login_required
def add_slip(request):
    if request.method == 'POST':
        form = PaymentSlipForm(request.POST)
        if form.is_valid():
            slip = form.save(commit=False)
            slip.profile = request.user.bnnprofile
            slip.save()
            messages.add_message(request, messages.SUCCESS, 'Payment slip successfully added')
            house = request.user.bnnprofile.house
            if get_week_slips(house=house).aggregate(sum=Sum('total_amount'))['sum'] > house.weekly_spending_warning:
                messages.add_message(request, messages.WARNING, 'Warning: You have overspent on your house budget.')
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
    return render(request, 'edit.html', {'title':'Edit Profile', 'form':form})


def house_settings(request):
    house = request.user.bnnprofile.house
    if request.method == 'POST':
        form = HouseForm(request.POST, instance=house)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'House settings successfully updated.')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = HouseForm(instance=house)
    return render(request, 'edit.html', {'title':'House Settings', 'form':form})