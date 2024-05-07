from django import forms
from . models import PaymentType

class OrderForm(forms.Form):
    
    name=forms.CharField(label='', max_length=50,
                         error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام'}))
    
    family=forms.CharField(label='', max_length=50,
                         error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی'}))
    
    email=forms.CharField(label='', max_length=250,
                         required=False,
                         widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل(اختیاری)'}))
    
    phone_number=forms.CharField(label='', max_length=11,
                         required=False,
                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره تلفن(اختیاری)'}))
    
    address=forms.CharField(label='',
                         error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                         widget=forms.Textarea(attrs={'class':'form-control','placeholder':'ادرس','rows':'3'}))
    
    description=forms.CharField(label='',
                         required=False,
                         widget=forms.Textarea(attrs={'class':'form-control','placeholder':' توضیحات(اختیاری) ','rows':'3'}))
    
    payment_type=forms.ChoiceField(label='',
                                 choices=[(item.pk,item) for item in PaymentType.objects.all()],
                                 widget=forms.RadioSelect())
    