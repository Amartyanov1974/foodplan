from django.contrib import admin

# Register your models here.

# Add adminsortable2.admin to sort images and description with drag
from .models import Foodstuff, MealPlan, Client, Recipe, FoodList, DishType, Image, Description


@admin.register(Foodstuff)
class FoodstuffAdmin(admin.ModelAdmin):
    fields = ('name', 'price', 'weight')

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    fields = ('menu_type', 'allergies', 'calories', 'number_of_meals')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ('meal_plan', 'user', 'subscription', 'subscription_expiration_date')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('menu_type', 'cooking_time', 'calories', 'fats', 'proteins', 'carbs')

@admin.register(FoodList)
class FoodListAdmin(admin.ModelAdmin):
    fields = ('recipe', 'food_name', 'weight')

@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'recipe')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('recipe', 'image', 'image_position')

@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    fields = ('recipe', 'text', 'text_position')
