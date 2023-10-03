from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator

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
    ('рыба и морепродукты', 'рыба и морепродукты'),
    ('мясо', 'мясо'),
    ('зерновые продукты', 'зерновые продукты'),
    ('продукты пчеловодства', 'продукты пчеловодства'),
    ('орехи и бобовые', 'орехи и бобовые'),
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
    category = models.CharField(max_length=21,
                                choices=CATEGORY_CHOICES,
                                verbose_name='Категория')

    class Meta:
        verbose_name = 'Все продукты'
        verbose_name_plural = 'Все продукты'

    def __str__(self) -> str:
        return f'{self.name} - {self.category}'


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

    @property
    def is_subscription_active(self):
        if timezone.now() < self.subscription_expiration_date:
            self.subscription = 'P'
            self.save()
            return True
        else:
            self.subscription = 'R'
            self.save()
            return False

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
        verbose_name='Cтатус оплаты',
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

@receiver(post_save, sender=Transaction)
def change_subscription_status(sender, instance, created, **kwargs):
    if instance.status == 'succeeded':
        client = instance.client
        subscription_expiration_date = instance.date + relativedelta(
                                        months=+int(instance.order_name))
        client.subscription_expiration_date = subscription_expiration_date
        client.save()


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
                              upload_to='', blank=True, null=True)
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


class Allergen(models.Model):
    name = models.CharField(verbose_name='Алергены',
                            max_length=50)

    class Meta:
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'

    def __str__(self):
        return str(self.name)


class DishType(models.Model):
    name = models.CharField(verbose_name='Тип блюда',
                            max_length=50)

    class Meta:
        verbose_name = 'Тип блюда'
        verbose_name_plural = 'Тип блюда'

    def __str__(self):
        return str(self.name)


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
    allergens = models.ManyToManyField(Allergen,
                                       verbose_name='Аллергены',
                                       related_name='meal_plans',
                                       blank=True)
    recipes = models.ManyToManyField(Recipe,
                                     verbose_name='Рецепты',
                                     related_name='meal_plans',
                                     blank=True)
    dish_types = models.ManyToManyField(DishType,
                                        verbose_name='Тип блюда',
                                        max_length=50)

    class Meta:
        verbose_name = 'План питания'
        verbose_name_plural = 'Планы питания'

    def __str__(self) -> str:
        return str(self.allergens)


#@receiver(post_save, sender=MealPlan)
#def save_meal_plan(sender, instance, created, **kwargs):
#    client = instance.client
#    if client:
#        subscription_expiration_date = instance.date + relativedelta(
#                                        months=+int(instance.order_name))
#        client.subscription_expiration_date = subscription_expiration_date
#        client.save()


class FoodItem(models.Model):
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                     related_name='food_items')
    food_names = models.ForeignKey(Foodstuff, on_delete=models.CASCADE,
                                        verbose_name='Продукты',
                                        related_name='food_items')
    weight = models.FloatField(verbose_name='Вес в граммах',
                               default=100,
                               validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Список продуктов'
        verbose_name_plural = 'Списки продуктов'
