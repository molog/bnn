from django import forms

from models import PaymentSlip, BnnProfile, House



class PaymentSlipForm(forms.ModelForm):
    class Meta:
        model = PaymentSlip
        exclude = ('profile')
        

class BnnProfileForm(forms.ModelForm):
    class Meta:
        model = BnnProfile
        fields = ['nick_name']
        
        
class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['weekly_spending_warning']
        