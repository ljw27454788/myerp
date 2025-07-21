from django.contrib import admin
from factory.models import Product, Machine

# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(Machine)
class Machine(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass