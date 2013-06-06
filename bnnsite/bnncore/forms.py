from django import forms

from models import PaymentSlip



class PaymentSlipForm(forms.ModelForm):
    class Meta:
        model = PaymentSlip
        exclude = ('profile')
        
