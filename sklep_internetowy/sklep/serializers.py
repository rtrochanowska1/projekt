from rest_framework import serializers
from .models import CoffeeTaste, Producent, Coffee, Customer, Order

class CoffeeTasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeTaste
        fields = ['id', 'name', ' description', 'coffee_strength', 'coffee_acidity']
        read_only_fields = ['id']


class ProducentSerializer(serializers.ModelSerializer):
    country_display = serializers.CharField(source='get_country_display', read_only=True)
    class Meta:
        model = Producent
        fields = ['id','name', 'country', 'country_display']
        read_only_fields = ['id', 'country_display']

    def validate_name(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Nazwa producenta powinna rozpoczynać się wielką literą!"
            )
        return value


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'type', 'taste', 'producent', 'price']
        read_only_fields = ['id']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'surname', 'email', 'phone_number', 'registration_date', 'loyalty_points']
        read_only_fields = ['id', 'registration_date', 'loyalty_points'] 

    def validate_name(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Imię musi zaczynać się wielką literą."
            )
        return value

    def validate_surname(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Nazwisko musi zaczynać się wielką literą."
            )
        return value



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'is_completed', 'transaction_id']
        read_only_fields = ['id', 'date_ordered']