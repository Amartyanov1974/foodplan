import string
from random import choice

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User


User._meta.get_field('email')._unique = True

def index(request):
    if 'user_name' in request.session:
        username = request.session['user_name']
        context = {
            'username': username,
            }
        return render(request, 'index.html', context=context)
    return render(request, 'index.html')


def lk(request):
    if 'user_name' in request.session:
        username = request.session['user_name']
        context = {
            'username': username,
            }
        return render(request, 'lk.html', context=context)
    return redirect('/')

def auth_message(request):
    context = {
        'message': request.session.get('message'),
        }
    request.session['message'] =''
    return render(request, 'auth.html', context=context)

def auth(request):
    """ Авторизация пользователя

    До авторизации request.user="AnonymousUser"
    После авторизации request.user=user(email)
    """
    if request.method == 'POST' and 'email' in request.POST and 'passwd' in request.POST:
        username = request.POST['email']
        password = request.POST['passwd']
        try:
            user = authenticate(username=username, password=password)
        except:
            user=None
        if not user:
            request.session['message'] = 'Ошибка авторизации'
            return redirect('auth_message')
        login(request, user)
        user = User.objects.get(username=username)
        request.session['user_name'] = user.first_name
        return redirect('/')
    return render(request, 'auth.html', )

def sendpasswd_message(request):
    context = {
        'message': request.session.get('message'),
        }
    request.session['message'] =''
    return render(request, 'sendpasswd.html', context=context)

def sendpasswd(request):
    """Генерация пароля и отправка по почте

    Для работы функции отправки пароля по почте необходимо в .env
    занести следующие параметры:
    EMAIL_HOST
    DEFAULT_FROM_EMAIL
    EMAIL_PORT
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    EMAIL_USE_SSL
    Подробности: https://djangodoc.ru/3.2/topics/email/
    """
    if request.method == 'POST' and 'email' in request.POST:
        email=request.POST['email']
        try:
            user = User.objects.get(email=email)
        except:
            request.session['message'] = 'Пользователь с такой почтой не зарегистрирован'
            return redirect('sendpasswd_message')
        chars = f'{string.ascii_letters}{string.digits}'
        new_passwd = ''.join([choice(chars) for i in range(7)])
        user.set_password(new_passwd)
        user.save()
        send_mail(
            'Новый пароль от Foodplane',
            f'Ваш новый пароль: {new_passwd}',
            '',
            [email,],
            fail_silently=False,
        )
        return redirect('auth')
    return render(request, 'sendpasswd.html', )


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
    """Регистрация

    Сохраняем имя в first_name объекта user,
    почту используем в качестве логина
    Проверяем подтвержение пароля и уникальность логина (почты)
    """
    if request.method == 'POST' and 'username' in request.POST:
        first_name = request.POST['username']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['passwd']
        passwordconfirm = request.POST['passwdconfirm']
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
                    first_name=first_name,
                    username=username,
                    password=password,
                    email=email,
                )
            except:
                request.session['message'] =  'Пользователь с такой почтой существует'
                return redirect('registration_message')
        login(request, user)
        request.session['user_name'] = first_name
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
