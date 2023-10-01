from django.conf import settings
from django.shortcuts import render, redirect
from .models import Transaction, Client
from yookassa import Configuration, Payment



def get_payment(request):
    Configuration.account_id = settings.SHOP_ACCOUNT_ID
    Configuration.secret_key = settings.SHOP_SECRET_KEY
    if request.GET:
        price = request.GET.get('price1')
        meal_plan = request.GET.get('meal_plan')
        username = request.GET.get('username')
        limitation = request.GET.get('limitation')
        path = request.build_absolute_uri('/')

        payment = Payment.create({
            "amount": {
                "value": f"{price}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{path}accept_payment/",
            },
            "capture": True,
            "description": f"Оплата подписки для пользователя {username}",
            "metadata": {
                "order_id": 1
            }
        })
        Transaction.objects.create(
            order_name=limitation.split()[0],
            client=Client.objects.get(user=request.user),
            transaction_id=payment.id,
            status=payment.status,
            price=price
        )
        return redirect(payment.confirmation.confirmation_url)
    return render(request, 'order.html')

def accept_payment(request):
    transaction = Transaction.objects.filter(client=Client.objects.get(user=request.user)).last()

    Configuration.account_id = settings.SHOP_ACCOUNT_ID
    Configuration.secret_key = settings.SHOP_SECRET_KEY
    payment_id = transaction.transaction_id
    payment = Payment.find_one(payment_id)
    transaction.status = payment.status
    transaction.save()
    transaction.client.is_subscription_active
    client = Client.objects.get(user=request.user)
    context = {
        'username': client.user_name,
        }
    return render(request, 'accept_payment.html', context=context)
