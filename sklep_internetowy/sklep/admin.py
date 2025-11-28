from django.contrib import admin
from .models import (
    Customer, Coffee, Producent, CoffeeTaste, Order)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "email", "loyalty_points", "registration_date"]
    readonly_fields = ('registration_date',) #tylko do odczytu
    list_filter = ["registration_date"]
    ordering = ('surname',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "date_ordered", "is_completed", "transaction_id"]
    readonly_fields = ('date_ordered',) #tylko do odczytu
    list_filter = ["is_completed", "date_ordered"]
    ordering = ('-date_ordered',) 


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ["name", "producent", "price", "type"]
    list_filter = ["producent", "type"]
    ordering = ('name',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Producent)
admin.site.register(CoffeeTaste)