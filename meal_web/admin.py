from django.contrib import admin
from .models import Meal, WeeklyMenu, MenuItem, Subscription, Order

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'diet_type', 'calories')
    list_filter = ('diet_type',)

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0

@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display = ('week_start',)
    inlines = [MenuItemInline]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'diet_preference', 'active', 'paused', 'paid', 'created_at')
    list_filter = ('diet_preference', 'active', 'paused', 'paid')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription', 'meal', 'date', 'status')
    list_filter = ('status',)
