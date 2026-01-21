from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import CoffeeTaste, Producent, Coffee, Customer, Order

class CoffeeTasteSerializer(serializers.ModelSerializer):
    """Serializator dla modelu CoffeeTaste"""
    class Meta:
        model = CoffeeTaste
        fields = ['id', 'name', 'description', 'coffee_strength', 'coffee_acidity']
        read_only_fields = ['id'] # pole id jest generowane automatycznie, użytkownik nie może go edytowac

class ProducentSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'type', 'taste', 'producent', 'price']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    """Serializator do rejestracji nowych użytkowników."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # tworzy nowego użytkownika z zaszyfrowanym hasłem
        return user

class CustomerSerializer(serializers.ModelSerializer):
    """Serializator dla modelu Customer"""
    class Meta:
        model = Customer
        fields = "__all__" # eksportuje wszystkie pola modelu
        read_only_fields = ['id', 'registration_date']

    def validate_name(self, value):
        if not (value[0].isupper() and value.isalpha()): # sprawdza czy imię zawiera tylko litery i zaczyna się wielką literą
            raise serializers.ValidationError("Imię powinno zawierać tylko litery i rozpoczynać się wielką literą.")
        return value

    def validate_surname(self, value):
        if not (value[0].isupper() and value.isalpha()): # sprawdza czy nazwisko zawiera tylko litery i zaczyna się wielką literą
            raise serializers.ValidationError("Nazwisko powinno zawierać tylko litery i rozpoczynać się wielką literą.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    """Serializator dla modelu Order"""
    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'is_completed', 'transaction_id']
        read_only_fields = ['id', 'date_ordered'] # uzytkownik nie moze edytowac