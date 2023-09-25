from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html',)

def lk(request):
    context = {}
    return render(request, 'lk.html', )

def auth(request):
    context = {}
    return render(request, 'auth.html', )

def registration(request):
    context = {}
    return render(request, 'registration.html', )

def order(request):
    context = {}
    return render(request, 'order.html', )

def card1(request):
    context = {}
    return render(request, 'card1.html', )

def card2(request):
    context = {}
    return render(request, 'card2.html', )

def card3(request):
    context = {}
    return render(request, 'card3.html', )
