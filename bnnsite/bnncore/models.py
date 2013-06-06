# -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User



class House(models.Model):
    name = models.CharField(max_length=100)
    
    
class BnnProfile(models.Model):
    user = models.OneToOneField(User)
    house = models.ForeignKey(House)
    nick_name = models.CharField(max_length=100, blank=True)
    

class PaymentSlip(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(BnnProfile, null=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid_date = models.DateField(default=datetime.date.today())
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField()
    
    class Meta:
        ordering = ['-paid_date', '-id']
    
    def __unicode__(self):
        return u'%s %s ￥%s' % (self.user, self.paid_date, self.total_amount)




from django.contrib import admin

admin.site.register(PaymentSlip)