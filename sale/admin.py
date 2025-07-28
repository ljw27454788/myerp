from django.contrib import admin
from sale.models import *

# Register your models here.
@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(Order)
class Order(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(SendInvoice)
class SendInvoice(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(SendOrder)
class SendOrder(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(PriceRecord)
class PriceRecord(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass

@admin.register(Sample)
class Sample(admin.ModelAdmin):
    readonly_fields = ('id',)
    pass