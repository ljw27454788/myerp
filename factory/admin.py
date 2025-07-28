from django.contrib import admin
from factory.models import *

# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(Machine)
class Machine(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(Client)
class Client(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass