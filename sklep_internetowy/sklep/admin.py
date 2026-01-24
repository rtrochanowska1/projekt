from django.contrib import admin
from .models import CoffeeTaste, Producent, Coffee, Customer, Order, OrderItem


@admin.register(CoffeeTaste) # rejestracja modelu CoffeeTaste w panelu admina
class CoffeeTasteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "coffee_strength", "coffee_acidity")
    search_fields = ("name",)


@admin.register(Producent) # rejestracja modelu Producent w panelu admina
class ProducentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(Coffee) # rejestracja modelu Coffee w panelu admina
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "producent", "coffeetype", "price", "taste")
    list_filter = ("coffeetype", "producent", "taste")
    search_fields = ("name",)


@admin.register(Customer) # rejestracja modelu Customer w panelu admina
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "phone_number", "registration_date")
    ordering = ("user__last_name", "user__first_name")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")

    @admin.display(ordering="user__username", description="Username") #
    def username(self, obj):
        return obj.user.username

    @admin.display(ordering="user__first_name", description="Imię")
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering="user__last_name", description="Nazwisko")
    def last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering="user__email", description="Email")
    def email(self, obj):
        return obj.user.email


@admin.register(Order) # rejestracja modelu Order w panelu admina
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date_ordered", "is_paid", "transaction_id")
    list_filter = ("is_paid", "date_ordered")
    search_fields = ("customer__user__username", "customer__user__email")
    date_hierarchy = "date_ordered"


@admin.register(OrderItem) # rejestracja modelu OrderItem w panelu admina
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "coffee", "quantity", "price_at_order", "date_added")
    list_filter = ("order", "coffee")