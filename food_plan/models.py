from django.db import models
from django.core import validators


class User(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('R', 'Regular'),
        ('P', 'Premium')
    ]

    subscription_type = models.CharField(verbose_name='Подписка',
                                         max_length=7,
                                         choices=SUBSCRIPTION_CHOICES,
                                         default='R')
    number_persons = models.IntegerField(verbose_name='Количество персон',
                                         default=1)
    email = models.EmailField(verbose_name='Email',
                              max_length=254,
                              validators=[validators.EmailValidator(
                                            message='Invalid Email')])
    subscription_expiration_date = models.DateField(
                                        verbose_name='Дата окончания подписки',
                                        null=True,
                                        blank=True,
                                        default=None)


class Recipe(models.Model):
    MENU_CHOICES = [
        ('Classic', 'Classic'),
        ('Low Сarb', 'Low Сarb'),
        ('Vegetarian', 'Vegetarian'),
        ('Keto', 'Keto'),
    ]
    menu_type = models.CharField(verbose_name='Тип меню',
                                 max_length=10,
                                 choices=MENU_CHOICES,
                                 default='Classic')
    cooking_time = models.IntegerField(verbose_name='Время приготовления, мин.')
    calories = models.IntegerField(verbose_name='Калорий на 100г.')
    fats = models.IntegerField(verbose_name='Жиров на 100г.')
    proteins = models.IntegerField(verbose_name='Белков на 100г.')
    carbs = models.IntegerField(verbose_name='Углеводов на 100г.')


    def calculate_budget(self):
        # Add budget calculation for each week
        pass


class Foodstuff(models.Model):
    name = models.CharField(verbose_name='Продукт',
                            max_length=200)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=6,
                                decimal_places=2)
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)


class FoodList(models.Model):
    recipe = models.ManyToManyField(Recipe,
                                    on_delete=models.SET_NULL,
                                    related_name='food_lists')
    food_name = models.ManyToManyField(Foodstuff,
                                       verbose_name='Продукт')
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)
    # Add unit price calculation for each list_of_products
    # depending on the number of persons


class DishType(models.Model):
    # examoles sauces,
    name = models.CharField(max_length=200,
                            verbose_name='Тип блюда')
    recipe = models.ManyToManyField(Recipe,
                                    on_delete=models.SET_NULL,
                                    related_name='dish_types')


class Image(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='images')
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='')
    image_position = models.IntegerField(verbose_name='Позиция картинки',
                                         null=False,
                                         blank=False,
                                         default=0)

    class Meta:
        ordering = ['image_position']


class Description(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='descriptions')
    text = models.TextField(verbose_name='Инструкция рецепта')
    text_position = models.IntegerField(verbose_name='Позиция текста',
                                        null=False,
                                        blank=False,
                                        default=0)

    class Meta:
        ordering = ['text_position']
