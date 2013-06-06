import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Sum

from models import PaymentSlip
from forms import PaymentSlipForm


@login_required
def summary(request):
    """ calculate the previous 2 weeks summary and any outstanding notifications"""
    today = datetime.date.today()
    week_day = today.weekday()
    this_week_slips = PaymentSlip.objects.filter(paid_date__gte=today - datetime.timedelta(days=week_day))
    last_week_slips = PaymentSlip.objects.filter(paid_date__gte=today - datetime.timedelta(days=week_day+7)).filter(paid_date__lt=today - datetime.timedelta(days=week_day))
    this_week_sum = sum([slip.total_amount for slip in this_week_slips])
    last_week_sum = sum([slip.total_amount for slip in last_week_slips])
    return render(request, 'summary.html', {'this_week_slips':this_week_slips, 
                                            'last_week_slips':last_week_slips,
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
    



