"""foodplan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from food_plan import views, payment_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('lk', views.lk, name='lk'),
    path('auth', views.auth, name='auth'),
    path('send', views.sendpasswd, name='send'),
    path('change_passwd', views.change_passwd, name='change_passwd'),
    path('change_passwd_message', views.change_passwd_message, name='change_passwd_message'),
    path('change_email', views.change_email, name='change_email'),
    path('change_email_message', views.change_email_message, name='change_email_message'),
    path('sendpasswd_message', views.sendpasswd_message, name='sendpasswd_message'),
    path('auth_message', views.auth_message, name='auth_message'),
    path('deauth', views.deauth, name='deauth'),
    path('registration', views.registration, name='registration'),
    path('registration_message', views.registration_message, name='registration_message'),
    path('order', views.order, name='order'),
    path('order_message', views.order_message, name='order_message'),
    path('card', views.card, name='card'),
    path('pay_card', views.pay_card, name='pay_card'),
    path('payment/', payment_views.get_payment, name='payment'),
    path('purchase', views.purchase, name='purchase'),
    path('accept_payment/', payment_views.accept_payment, name='accept_payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
