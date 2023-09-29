from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


User._meta.get_field('email')._unique = True


class Foodstuff(models.Model):
    name = models.CharField(verbose_name='Продукт',
                            max_length=200)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=6,
                                decimal_places=2)
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)

    class Meta:
        verbose_name = 'Все продукты'
        verbose_name_plural = 'Все продукты'


class Client(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('R', 'Regular'),
        ('P', 'Premium')
    ]
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


class MealPlan(models.Model):
    client = models.OneToOneField(Client,
                                  verbose_name='Клиент',
                                  on_delete=models.CASCADE,
                                  related_name='meal_plan',
                                  blank=False,
                                  null=True)
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
    number_persons = models.IntegerField(verbose_name='Количество персон',
                                         default=1)
    allergies = models.ManyToManyField(
                    Foodstuff,
                    verbose_name='Продукты, на которые есть алергия',
                    related_name='meal_plans',
                    blank=True,
                    default=None)
    CALORIE_CHOICES = [
        ('1000', 'Basic'),
        ('1400', 'Fit'),
        ('1800', 'Balance'),
    ]
    calories = models.CharField(verbose_name='Калорий в день',
                                max_length=7,
                                choices=CALORIE_CHOICES,
                                default='1800')
    MEAL_NUMBER_CHOICES = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]
    number_of_meals = models.CharField(max_length=1,
                                       verbose_name='Приемов пищи в день',
                                       choices=MEAL_NUMBER_CHOICES,
                                       default='3')

    class Meta:
        verbose_name = 'План питания'
        verbose_name_plural = 'Планы питания'

    def __str__(self) -> str:
        return str(self.allergies)


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
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин.')
    calories = models.IntegerField(verbose_name='Калорий на 100г.')
    fats = models.IntegerField(verbose_name='Жиров на 100г.')
    proteins = models.IntegerField(verbose_name='Белков на 100г.')
    carbs = models.IntegerField(verbose_name='Углеводов на 100г.')
    meal_plans = models.ManyToManyField(MealPlan,
                                        verbose_name='Планы питания',
                                        related_name='recipes')

    def calculate_budget(self):
        # Add budget calculation for each week
        pass

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'



class FoodList(models.Model):
    recipes = models.ManyToManyField(Recipe,
                                     related_name='food_lists')
    food_names = models.ManyToManyField(Foodstuff,
                                        verbose_name='Продукты',
                                        related_name='food_lists')
    weight = models.FloatField(verbose_name='Вес в кг',
                               default=0.1)
    # Add unit price calculation for each list_of_products
    # depending on the number of persons

    class Meta:
        verbose_name = 'Список продуктов'
        verbose_name_plural = 'Списки продуктов'



class DishType(models.Model):
    # examples sauces, soups etc.
    name = models.CharField(max_length=200,
                            verbose_name='Тип блюда')
    recipes = models.ManyToManyField(Recipe,
                                     related_name='dish_types')

    class Meta:
        verbose_name = 'Разновидность бюда'
        verbose_name_plural = 'Разновидности блюд'


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
        verbose_name = 'Картинка рецепта'
        verbose_name_plural = 'Картинки рецептов'


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
        verbose_name = 'Описание рецепта'
        verbose_name_plural = 'Описания рецептов'
