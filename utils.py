from kavenegar import *
import os
from uuid import uuid4
import random


def crete_random(count): #تابع تولید رندوم کدفعال سازی
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)


def send_sms1(mobile_number,active_code): #تابع ارسال کد فعال سازی
    # try:
    #     api = KavenegarAPI('495079705A4F734F445551616B3658382F2B4976654B59346E376C6455416E6866494A5A775478345A63493D')
    #     params = {
    #         'sender': '',#optional
    #         'receptor':mobile_number,#multiple mobile number, split by comma
    #         'message': active_code,
    #     } 
    #     response = api.sms_send(params)
    #     return response
    # except APIException as e: 
    #     print(e)
    # except HTTPException as e: 
    #     print(e)
    pass

class FileUpload:
    def __init__(self,dir,perfix):
        self.dir=dir
        self.perfix=perfix
    
    def upload_to(self,instance,filename):
        name,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.perfix}/{uuid4()}{ext}'
    
def reaplace_dash_to_space(name):
        new_title="".join([eliminator.replace(" ","-") for eliminator in name])
        return new_title.lower()

def price_by_delivery_tax(price,discount=0):
    delivery=25000
    if price>=500000:
        delivery=0
    tax=(price+delivery)*(9/100)
    sum=price+delivery+tax
    sum=sum-(sum*discount/100)
    return int(sum),delivery,int(tax)

