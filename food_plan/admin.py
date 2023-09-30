from django.contrib import admin
from food_plan.models import (Client, MealPlan, FoodList,
                              Foodstuff, Recipe, DishType, Transaction)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['menu_type', 'cooking_time', 'calories',
                    'fats', 'proteins', 'carbs']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'subscription',
                    'subscription_expiration_date']
    readonly_fields = ['user']


@admin.register(FoodList)
class FoodListAdmin(admin.ModelAdmin):
    pass


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Foodstuff)
class FoodstuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'weight', 'category']


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['client', 'menu_type', 'number_persons',
                    'calories', 'number_of_meals']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['order_name', 'date']
