import string
from random import choice
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from food_plan.models import Client, Recipe, MealPlan, Allergen, DishType
from django.conf import settings

User._meta.get_field('email')._unique = True


def get_meal_plan(client):
    try:
        meal_plan = MealPlan.objects.get(client=client)
    except:
        return False
    result = {
        'menu_type': meal_plan.menu_type,
        'number_persons': meal_plan.number_persons,
        'allergens': [allergen for allergen in meal_plan.allergens.get_queryset()],
        'dish_types': [dish_type for dish_type in meal_plan.dish_types.get_queryset()]
    }
    return result

def index(request):
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }
        return render(request, 'index.html', context=context)
    return render(request, 'index.html')


def lk(request):
    if 'user_name' in request.session:
        client = Client.objects.get(user=request.user)
        meal_plan = get_meal_plan(client)

        context = {
            'username': request.session['user_name'],
            'client': client,
            'meal_plan': meal_plan
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

def deauth(request):
    logout(request)
    request.session['user_name'] = ''
    return redirect('/')

def change_passwd_message(request):
    context = {
        'message': request.session.get('message'),
        'username': request.user.first_name,
        'email': request.user.email,
        }
    request.session['message'] =''
    return render(request, 'lk.html', context=context)

def change_passwd(request):
    if request.method == 'POST' and 'passwd' in request.POST:
        passwd=request.POST['passwd']
        passwdconfirm=request.POST['passwdconfirm']
        if passwd != passwdconfirm or len(passwd)<1:
            request.session['message'] = 'Пароли не совпадают или поля не заполнены'
            return redirect('change_passwd_message')
        user = User.objects.get(email=request.user)
        user.set_password(passwd)
        user.save()
        request.session['user_name'] = ''
        return redirect('/')
    return redirect('lk')

def change_email_message(request):
    context = {
        'message': request.session.get('message'),
        'username': request.user.first_name,
        'email': request.user.email,
        }
    request.session['message'] =''
    return render(request, 'lk.html', context=context)

def change_email(request):
    if request.method == 'POST' and 'email' in request.POST:
        email=request.POST['email']
        try:
            user = User.objects.get(email=request.user)
            user.username = email
            user.email = email
            user.save()
        except:
            request.session['message'] = 'Такая почта уже зарегистрирована'
            return redirect('change_email_message')
        request.session['user_name'] = ''
        return redirect('/')
    return redirect('lk')


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
        try:
            user.set_password(new_passwd)
            user.save()
            send_mail(
                'Новый пароль от Foodplane',
                f'Ваш новый пароль: {new_passwd}',
                '',
                [email,],
                fail_silently=False,
            )
            request.session['message'] = 'Пароль выслан на вашу почту'
            return redirect('auth_message')
        except:
            request.session['message'] = 'Сбой отправки почты'
            return redirect('auth_message')
    return render(request, 'sendpasswd.html', )

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
                client = Client.objects.create(
                    user=user,
                )
            except:
                request.session['message'] =  'Пользователь с такой почтой существует'
                return redirect('registration_message')
        login(request, user)
        request.session['user_name'] = first_name
        return redirect('/')

    return render(request, 'registration.html' )

def order_message(request):
    client = Client.objects.get(user=request.user)
    context = {
        'message': request.session.get('message'),
        'username': client.user_name,
        }
    request.session['message'] =''
    return render(request, 'order.html', context=context)

def order(request):
    if not request.user.is_authenticated or request.user.username=='root':
        return redirect('auth')
    client = Client.objects.get(user=request.user)
    context = {
        'username': client.user_name,
        }
    return render(request, 'order.html', context=context)

def card(request):
    """
    Бесплатный рецепт
    """
    if not request.user.is_authenticated:
        return redirect('auth')
    client = Client.objects.get(user=request.user)
    recipes = Recipe.objects.filter(is_free=True)
    try:
        recipe = choice(recipes)
        ingredients = recipe.food_items.all()
    except:
        recipe = ''
        ingredients = ''

    context = {
        'username': request.session['user_name'],
        'recipe': recipe,
        'ingredients': ingredients,

        }
    return render(request, 'card.html', context=context)


def pay_card(request):

    if not request.user.is_authenticated:
        return redirect('auth')
    client = Client.objects.select_related('meal_plan').get(user=request.user)
    if client.subscription_expiration_date<datetime.now().date():
        return redirect('/')
    foodtype_dict = {'Вегетарианское': 'Vegetarian', 'Кето': 'Keto', 'Низкоуглеводное': 'Low Сarb', 'Классическое': 'Classic'}
    recipes = Recipe.objects.filter(menu_type__exact=foodtype_dict[client.meal_plan.menu_type])

    for recipe in recipes:
        out = False
        ingredients = recipe.food_items.all()
        for allergen in allergens:
            for ingredient in ingredients:
                if ingredient.food_names.category==str(allergen).lower():
                    out = True
                    break
            if out:
                break
        if out:
            continue
        recipes_done.append(recipe)

    try:
        recipe = choice(recipes_done)
        ingredients = recipe.food_items.all()
    except:
        recipe = ''
        ingredients = ''

    context = {
        'username': request.session['user_name'],
        'recipe': recipe,
        'ingredients': ingredients,

        }
    return render(request, 'pay_card.html', context=context)

def purchase(request):
    if not request.user.is_authenticated or request.user.username=='root':
        return redirect('auth')
    client = Client.objects.get(user=request.user)
    if not 'foodtype' in request.POST:
        request.session['message'] = 'Выберите тип меню'
        return redirect('order_message')
    if request.method == 'POST' and not 'price' in request.POST:
        foodtype = request.POST['foodtype']
        limitation = request.POST['limitation']
        meal = []
        breakfast = int(request.POST['breakfast'])
        if breakfast: meal.append('Завтрак')
        lunch = int(request.POST['lunch'])
        if lunch: meal.append('Обед')
        dinner = int(request.POST['dinner'])
        if dinner: meal.append('Ужин')
        dessert = int(request.POST['dessert'])
        if dessert: meal.append('Десерт')
        number_persons = int(request.POST['number_persons'])
        allergy = []
        # Рыба и морепродукты
        allergy1 = bool(request.POST.get('allergy1', False))
        if allergy1: allergy.append('рыба и морепродукты')
        # Мясо
        allergy2 = bool(request.POST.get('allergy2', False))
        if allergy2: allergy.append('мясо')
        # Зерновые
        allergy3 = bool(request.POST.get('allergy3', False))
        if allergy3: allergy.append('зерновые продукты')
        # Продукты пчеловодства
        allergy4 = bool(request.POST.get('allergy4', False))
        if allergy4: allergy.append('продукты пчеловодства')
        # Орехи и бобовые
        allergy5 = bool(request.POST.get('allergy5', False))
        if allergy5: allergy.append('орехи и бобовые')
        # Молочные продукты
        allergy6 = bool(request.POST.get('allergy6', False))
        if allergy6: allergy.append('молочные продукты')
        if not allergy: allergy.append('Нет')
        # Вместо 'Нет' пустого списка хватит

        """
        Здесь нужно выбрать рецепты и посчитать стоимость плана питания
        """
        price_list = {
            '1 мес.': 500,
            '3 мес.': 1400,
            '6 мес.': 2550,
            '12 мес.': 4800
        }

        # Все параметры выбора рецептов в одном словаре, вдруг понадобиться
        # description = {'foodtype': foodtype, 'limitation': limitation,
                       # 'breakfast': breakfast, 'lunch': lunch,
                       # 'dinner':dinner, 'dessert': dessert,
                       # 'number_persons': number_persons, 'allergy1': allergy1,
                       # 'allergy2' :allergy2, 'allergy3': allergy3,
                       # 'allergy4': allergy4, 'allergy5': allergy5,
                       # 'allergy6': allergy6}
        # print(description)

        foodtype_dict = {'veg': 'Вегетарианское', 'keto': 'Кето', 'low': 'Низкоуглеводное', 'classic': 'Классическое'}
        meal_plan = {
            "food_type": foodtype_dict[foodtype],
            "limitation": limitation,
            "number_persons": number_persons,
            "allergy": allergy,
            "meal": meal
        }

        descriptions = f'Тип питания: {foodtype_dict[foodtype]}, срок: {limitation}, Количество персон: {number_persons}, Аллергия: {allergy}, Количество приемов пищи: {meal}'
        price = price_list[f'{meal_plan["limitation"]}']
        context = {
            'username': client.user_name,
            'descriptions': descriptions,
            'price': price,
            'meal_plan': meal_plan,
            'limitation': limitation
            }
        # Сохраняем все критерии meal_plan в БД
        get_or_create_meal_plan(meal_plan=meal_plan, client=client)

        # context.update({'descriptions': descriptions})
        return render(request, 'order.html', context=context)


def get_or_create_meal_plan(meal_plan: dict, client: Client) -> MealPlan:
    menu_type = meal_plan['food_type']
    number_persons = meal_plan['number_persons']
    allergens = list(Allergen.objects.filter(name__in=meal_plan['allergy']))
    dish_types = list(DishType.objects.filter(name__in=meal_plan['meal']))
    meal_plan, created = MealPlan.objects.get_or_create(
                            client=client,
                            menu_type=menu_type,
                            number_persons=number_persons
    )
    meal_plan.allergens.set(allergens)
    meal_plan.dish_types.set(dish_types)
    return meal_plan
