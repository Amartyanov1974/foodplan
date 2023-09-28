from django.conf import settings
from django.shortcuts import render, redirect
from yookassa import Configuration, Payment


def get_payment(request):
    Configuration.account_id = settings.SHOP_ACCOUNT_ID
    Configuration.secret_key = settings.SHOP_SECRET_KEY
    if request.GET:
        payment = Payment.create({
            "amount": {
                "value": "100.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/accept_payment/",
            },
            "capture": True,
            "description": "Заказ №1",
            "metadata": {
                "order_id": 1
            }
        })
        context = payment
        return redirect(payment.confirmation.confirmation_url)
    return render(request, 'order.html')

def accept_payment(request):
    return render(request, 'accept_payment.html')
