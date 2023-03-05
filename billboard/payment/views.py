from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings

import datetime
import json
import requests
import uuid
import os
from .functions import get_max

from .models import *
# Create your views here.

def home(request):
    message , price = get_max()
    return render(request, 'index.html', context = {"home":True,"message":message , "price":price})

# def exchanged_rate(amount):
#     url = "https://www.blockonomics.co/api/price?currency=USD"
#     r = requests.get(url)
#     response = r.json()
#     return amount/response['price']

def track_invoice(request, pk):
    invoice_id = pk
    invoice = Invoice.objects.get(id=invoice_id)
    data = {
            'order_id':invoice.order_id,
            # 'value':invoice.product.price,
            'addr': invoice.address,
            'status':Invoice.STATUS_CHOICES[invoice.status+1][1],
            'invoice_status': invoice.status,
        }
    if (invoice.received):
        bid_ = invoice.bid
        data['paid'] =  invoice.received/1e8
        bid_.price = data['paid']
        bid_.save()
        invoice.bid = bid_
        invoice.save()
    else:
        data['paid'] = 0 

    message , price = get_max()
    return render(request, 'index.html', context = {"home":False,"data":data,"max":price})
    # return render(request,'invoice.html',context=data)

def create_payment(request):
    mes = request.POST["message"]
    url = 'https://www.blockonomics.co/api/new_address'
    headers = {'Authorization': "Bearer " + settings.API_KEY}
    r = requests.post(url, headers=headers)
    bid_ = Bid(message = mes , price = 0)
    bid_.save()
    print(r.json())
    if r.status_code == 200:
        address = r.json()['address']
        order_id = uuid.uuid1()
        invoice = Invoice.objects.create(order_id=order_id,
                                address=address, bid=bid_)
        return HttpResponseRedirect(reverse('payment:track_payment', kwargs={'pk':invoice.id}))
    else:
        print(r.status_code, r.text)
        return HttpResponse("Some Error, Try Again!")
    
def receive_payment(request):
    
    # if (request.method != 'GET'):
    #     return 
    print(request.body)
    
    txid  = request.GET.get('txid')
    value = request.GET.get('value')
    status = request.GET.get('status')
    addr = request.GET.get('addr')

    invoice = Invoice.objects.get(address = addr)
    
    invoice.status = int(status)
    if (int(status) == 2):
        invoice.received = value
    invoice.txid = txid
    invoice.save()
    return HttpResponse(200)