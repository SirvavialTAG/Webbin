from django.contrib import admin
from .models import Brands, Cars

@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['country', 'brand']
    search_field = ['country', 'brand']

@admin.register(Cars)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color', 'power_volume']
    search_field = ['model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color', 'power_volume']
