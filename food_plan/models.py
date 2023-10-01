from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html

User._meta.get_field('email')._unique = True


DISH_CHOICES = [
    ('breakfast', 'breakfast'),
    ('lunch', 'lunch'),
    ('dinner', 'dinner'),
    ('dessert', 'dessert'),
]

CALORIE_CHOICES = [
    ('Basic 1000', 'Basic'),
    ('Fit 1400', 'Fit'),
    ('Balance 1800', 'Balance'),
]

CATEGORY_CHOICES = [
    ('рыба', 'рыба'),
    ('мясо', 'мясо'),
    ('зерновые продукты', 'зерновые продукты'),
    ('продукты пчеловодства', 'продукты пчеловодства'),
    ('орехи', 'орехи'),
    ('бобовые продукты', 'бобовые продукты'),
    ('молочные продукты', 'молочные продукты'),
]

ORDER_CHOICES = [
    ('1', '1 мес.'),
    ('3', '3 мес.'),
    ('6', '6 мес.'),
    ('12', '12 мес.'),
]

SUBSCRIPTION_CHOICES = [
    ('R', 'Regular'),
    ('P', 'Premium'),
]

MENU_CHOICES = [
    ('Classic', 'Classic'),
    ('Low Сarb', 'Low Сarb'),
    ('Vegetarian', 'Vegetarian'),
    ('Keto', 'Keto'),
]


class Foodstuff(models.Model):
    name = models.CharField(verbose_name='Продукт',
                            max_length=200)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=6,
                                decimal_places=2)
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)
    category = models.CharField(max_length=21,
                                choices=CATEGORY_CHOICES,
                                verbose_name='Категория')

    class Meta:
        verbose_name = 'Все продукты'
        verbose_name_plural = 'Все продукты'

    def __str__(self) -> str:
        return str(self.name)


class Client(models.Model):
    user = models.OneToOneField(User,
                                verbose_name='Пользователь',
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='client')
    subscription = models.CharField(verbose_name='Подписка',
                                    max_length=7,
                                    choices=SUBSCRIPTION_CHOICES,
                                    default='R')
    subscription_expiration_date = models.DateField(
                                        verbose_name='Дата окончания подписки',
                                        null=True,
                                        blank=True,
                                        default=None)

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_name(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.user_name} {self.user_email}'


class Transaction(models.Model):
    order_name = models.CharField(verbose_name='Название подписки',
                                  choices=ORDER_CHOICES,
                                  max_length=8)
    date = models.DateTimeField(verbose_name='Дата платежа',
                            default=timezone.now,
                            db_index=True)

    client = models.ForeignKey(Client,
                                    verbose_name='Клиент',
                                    related_name='transaction',
                                    on_delete=models.CASCADE)
    transaction_id = models.CharField(
        verbose_name='id транзакции',
        max_length=40,
        null=True
    )
    status = models.CharField(
        verbose_name='статус оплаты',
        max_length=40,
        null=True
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=6,
        decimal_places=0,
        null=True
    )

    class Meta:
        ordering = ['date']
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class Recipe(models.Model):
    name = models.CharField(max_length=250,
                            verbose_name='Название рецепта')
    menu_type = models.CharField(verbose_name='Тип меню',
                                 max_length=10,
                                 choices=MENU_CHOICES,
                                 default='Classic')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин.')
    calories = models.IntegerField(verbose_name='Калорий на 100г.')
    fats = models.IntegerField(verbose_name='Жиров на 100г.')
    proteins = models.IntegerField(verbose_name='Белков на 100г.')
    carbs = models.IntegerField(verbose_name='Углеводов на 100г.')
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='')
    text = models.TextField(verbose_name='Инструкция рецепта')
    is_free = models.BooleanField(verbose_name='Бесплатный рецепт',
                                  default=False)

    def preview_image(self):
        return format_html('<img src="{}" height="200" />', self.image.url)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class MealPlan(models.Model):
    client = models.OneToOneField(Client,
                                  verbose_name='Клиент',
                                  on_delete=models.CASCADE,
                                  related_name='meal_plan',
                                  blank=False,
                                  null=True)
    menu_type = models.CharField(verbose_name='Тип меню',
                                 max_length=10,
                                 choices=MENU_CHOICES,
                                 default='Classic')
    number_persons = models.IntegerField(verbose_name='Количество персон',
                                         default=1)
    allergies = models.ManyToManyField(
                    Foodstuff,
                    verbose_name='Продукты, на которые есть алергия',
                    related_name='meal_plans',
                    blank=True,
                    default=None)
    calories = models.CharField(verbose_name='Калорий в день',
                                max_length=12,
                                choices=CALORIE_CHOICES,
                                default='Balance 1800')
    recipes = models.ManyToManyField(Recipe,
                                     verbose_name='Рецепты',
                                     related_name='meal_plans')
    dish_type = models.CharField(verbose_name='Тип блюда',
                                 choices=DISH_CHOICES,
                                 max_length=9)

    class Meta:
        verbose_name = 'План питания'
        verbose_name_plural = 'Планы питания'

    def __str__(self) -> str:
        return str(self.allergies)


class FoodList(models.Model):
    recipes = models.ManyToManyField(Recipe,
                                     related_name='food_lists')
    food_names = models.ManyToManyField(Foodstuff,
                                        verbose_name='Продукты',
                                        related_name='food_lists')
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)

    class Meta:
        verbose_name = 'Список продуктов'
        verbose_name_plural = 'Списки продуктов'
