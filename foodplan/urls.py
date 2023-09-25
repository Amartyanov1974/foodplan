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
from food_plan import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('lk.html', views.lk, name='lk'),
    path('auth.html', views.auth, name='auth'),
    path('registration.html', views.registration, name='registration'),
    path('order.html', views.order, name='order'),
    path('card1.html', views.card1, name='card1'),
    path('card2.html', views.card2, name='card2'),
    path('card3.html', views.card3, name='card3'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
