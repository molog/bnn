from django import forms

from models import PaymentSlip, BnnProfile



class PaymentSlipForm(forms.ModelForm):
    class Meta:
        model = PaymentSlip
        exclude = ('profile')
        

class BnnProfileForm(forms.ModelForm):
    class Meta:
        model = BnnProfile
        fields = ['nick_name']