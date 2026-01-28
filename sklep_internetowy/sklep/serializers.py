from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import CoffeeTaste, Producent, Coffee, Customer, Order, OrderItem

class RegisterSerializer(serializers.ModelSerializer):
    """Serializator do rejestracji użytkowników."""
    password = serializers.CharField(write_only=True, min_length=6) # wymaga hasła o minimalnej długości 6 znaków
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # tworzy nowego użytkownika z zaszyfrowanym hasłem

class CoffeeTasteSerializer(serializers.ModelSerializer): 
    """Serializator dla modelu CoffeeTaste."""
    class Meta:
        model = CoffeeTaste
        fields = ['id', 'name', 'description', 'coffee_strength', 'coffee_acidity']
        read_only_fields = ['id']

class ProducentSerializer(serializers.ModelSerializer): #serializer dla modelu Producent
    """Serializator dla modelu Producent"""
    country_display = serializers.CharField(source='get_country_display', read_only=True)
    class Meta:
        model = Producent
        fields = ['id','name', 'country', 'country_display']
        read_only_fields = ['id', 'country_display']

    def validate_name(self, value): # sprawdza czy nazwa producenta zaczyna się wielką literą.
        if not value[0].isupper():
            raise serializers.ValidationError("Nazwa producenta powinna rozpoczynać się wielką literą.")
        return value

class CoffeeSerializer(serializers.ModelSerializer):
    """Serializator dla modelu Coffee."""
    coffee_type_display = serializers.CharField(source='get_coffeetype_display', read_only=True)
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'coffeetype', 'coffee_type_display', 'taste', 'producent', 'price']
        read_only_fields = ['id', 'coffee_type_display']
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cena musi być większa od zera.")
        return value

class CustomerSerializer(serializers.ModelSerializer): 
    """Serializator dla profilu klienta."""
    class Meta:
        model = Customer
        fields = [ 'id', 'user', 'phone_number', 'registration_date']
        read_only_fields = ['id', 'user', 'registration_date']

    def validate_phone_number(self, value): # sprawdza czy numer telefonu ma co najmniej 9 znaków
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Numer telefonu może zawierać tylko cyfry.")
            if len(value) != 9:
                raise serializers.ValidationError("Numer telefonu musi mieć dokładnie 9 cyfr.")
        return value

class OrderItemSerializer(serializers.ModelSerializer): #serializer dla modelu OrderItem
    """Serializator dla pozycji zamówienia."""
    coffee_name = serializers.CharField(source='coffee.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'coffee', 'coffee_name', 'quantity', 'price_at_order', 'date_added']
        read_only_fields = ['id', 'date_added', 'coffee_name']
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ilość musi być większa od zera.")
        return value
    def validate_price_at_order(self, value):
        if value < 0:
            raise serializers.ValidationError("Cena musi być większa od zera.")
        return value
    
class OrderSerializer(serializers.ModelSerializer): #serializer dla modelu Order
    """Serializator dla modelu Order."""
    customer_name = serializers.CharField(source='customer.__str__', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'date_ordered', 'is_paid', 'transaction_id', 'items']
        read_only_fields = ['id', 'date_ordered', 'customer','customer_name', 'items']