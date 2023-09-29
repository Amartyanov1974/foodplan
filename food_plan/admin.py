from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from food_plan.models import (Client, MealPlan, FoodList, Foodstuff,
                              Recipe, DishType, Image, Description)



class ImageInline(SortableStackedInline):
    '''Inline for images to show in Place model'''
    model = Image
    readonly_fields = ['preview']

    def preview(self, obj):
        '''display preview of image'''
        return format_html('<img src="{}" width="200" height="200" />',
                           obj.image.url)


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['menu_type', 'cooking_time', 'calories',
                    'fats', 'proteins', 'carbs']
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    '''Admin panel for Image model'''
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'subscription_expiration_date',
                    'meal_plan']


@admin.register(FoodList)
class FoodListAdmin(admin.ModelAdmin):
    pass


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'text', 'text_position']


@admin.register(Foodstuff)
class FoodstuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'weight']


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['menu_type', 'number_persons',
                    'calories', 'number_of_meals']
