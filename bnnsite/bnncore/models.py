# -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PaymentSlip(models.Model):
    user = models.ForeignKey(User)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid_date = models.DateField(default=datetime.date.today())
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s %s ￥%s' % (self.user, self.paid_date, self.total_amount)



from django.contrib import admin

admin.site.register(PaymentSlip)