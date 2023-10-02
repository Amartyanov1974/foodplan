import os
import json
import argparse
from random import choice, sample
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from urllib.parse import urlparse
from food_plan.models import Foodstuff, Allergen, Recipe, DishType, FoodItem


def save_image(recipe, img_url):
    response = requests.get(img_url)
    response.raise_for_status
    img = ContentFile(response.content)
    img_path = urlparse(img_url)
    img_name = os.path.basename(img_path.path)
    recipe.image.save(img_name, img, save=True)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Количество сгенерированных рецептов')

    def handle(self, *args, **options):
        count = options['count']

        allergens = ['Рыба и морепродукты', 'Мясо', 'Зерновые',
                     'Продукты пчеловодства', 'Орехи и бобовые',
                     'Молочные продукты']
        dishtypes = ['Завтрак', 'Обед', 'Ужин', 'Десерт']

        for allergen in allergens:
            allerg, created = Allergen.objects.update_or_create(name=allergen)
            print(allerg, created)
        for dishtype in dishtypes:
            disht, created = DishType.objects.update_or_create(name=dishtype)
            print(disht, created)
        menu = ['Classic', 'Low Сarb', 'Vegetarian', 'Keto']
        cooking_time = [15, 20, 25, 30, 35, 45, 50]
        calories = [1000, 1500, 2000, 2500, 3000, 3500, 4000]
        fats = [5, 10, 15, 20, 25]
        proteins = [5, 10, 15, 20]
        carbs = [30, 35, 40, 45, 50]
        image_url = ['https://amartyanov.ru/media/fish_roll.jpg', 'https://amartyanov.ru/media/shrimp_roll.jpg', 'https://amartyanov.ru/media/long_chiz.jpg']

        for num in range(count):
            name_item = f'Рецепт номер {num}'
            menu_item = choice(menu)
            cooking_time_item = choice(cooking_time)
            calories_item = choice(calories)
            fats_item = choice(fats)
            proteins_item = choice(proteins)
            carbs_item = choice(carbs)
            img_url_item = choice(image_url)
            text = f'{name_item} входит в {menu_item} меню. Содержит на 100 гр. {fats_item} жиров, {proteins_item} белков, {carbs_item} углеводов. Готовится в течении {cooking_time_item}-ти минут.'

            recipe, created = Recipe.objects.update_or_create(
                name=name_item,
                defaults={'cooking_time': cooking_time_item, 'calories': calories_item, 'text': text,
                          'fats': fats_item, 'proteins': proteins_item, 'carbs' :carbs_item, })
            print(recipe, created)
            if created:
                img_url=img_url_item
                save_image(recipe, img_url)
                print(f'В базу добавили {recipe.name}')

        category = ['рыба', 'мясо', 'зерновые продукты', 'продукты пчеловодства', 'орехи', 'бобовые продукты', 'молочные продукты', 'зелень', 'птица', 'овощи', 'фрукты']

        for num in range(3*count):
            name_item = f'Продукт номер {num}'
            category_item = choice(category)
            foodstuff, created = Foodstuff.objects.update_or_create(
                name=name_item,
                defaults={'category': category_item})
            print(foodstuff, created)

        recipies = Recipe.objects.all()
        foodstuffes = Foodstuff.objects.all()
        weight = [100, 150, 200, 250, 300, 350, 400]

        for recipe in recipies:
            foodstuff = sample(list(foodstuffes), 4)
            for foodstuff_item in foodstuff:
                weight_item = choice(weight)

                foodlist, created = FoodItem.objects.update_or_create(
                    food_names=foodstuff_item, recipes=recipe,
                    weight=weight_item)
                print(foodlist, created)
