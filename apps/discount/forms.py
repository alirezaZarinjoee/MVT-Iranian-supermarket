from django import forms
class CouponForm(forms.Form):
    coupon_code=forms.CharField(label='', required=False,
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد تخفیف'}))
    