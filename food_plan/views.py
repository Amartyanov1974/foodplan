from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User


def index(request):
    if 'user_name' in request.session:
        username = request.session['user_name']
        context = {
            'username': username,
            }
    return render(request, 'index.html', context=context)

def lk(request):
    context = {}
    return render(request, 'lk.html', )

def auth(request):

    context = {}
    return render(request, 'auth.html', )

def deauth(request):
    logout(request)
    request.session['user_name'] = ''
    return redirect('/')

def registration_message(request):
    context = {
        'message': request.session.get('message'),
        }
    request.session['message'] =''
    return render(request, 'registration.html', context=context)

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwd']
        passwordconfirm = request.POST['passwdconfirm']
        email = request.POST['email']
        if password != passwordconfirm:
            request.session['message'] = 'Пароли не совпадают'
            return redirect('registration_message')
        try:
            user = authenticate(username=username, password=password)
        except:
            user=None
        if not user:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                )
            except:
                request.session['message'] =  'Пользователь с таким именем существует'
                return redirect('registration_message')
        login(request, user)
        request.session['user_name'] = username
        return redirect('/')

    return render(request, 'registration.html' )

def order(request):
    context = {}
    return render(request, 'order.html' )

def card1(request):
    context = {}
    return render(request, 'card1.html', )

def card2(request):
    context = {}
    return render(request, 'card2.html', )

def card3(request):
    context = {}
    return render(request, 'card3.html', )
