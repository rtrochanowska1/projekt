from django import forms
import re
from .models import Coffee, Producent, CoffeeTaste, Customer, User

class CoffeeForm(forms.ModelForm): # formularz do dodawania/edycji kawy
    class Meta:
        model = Coffee
        fields = [
            "name",
            "coffeetype",
            "price",
            "producent",
            "taste",
        ]
class ProducentForm(forms.ModelForm): # formularz do dodawania/edycji producenta
    class Meta:
        model = Producent
        fields = ["name", "country"]  

class CoffeeTasteForm(forms.ModelForm): # formularz do dodawania/edycji smaku kawy
    class Meta:
        model = CoffeeTaste
        fields = ["name", "description", "coffee_strength", "coffee_acidity"]

class UserProfileForm(forms.ModelForm): # formularz do edycji danych użytkownika
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class CustomerProfileForm(forms.ModelForm): # formularz do edycji danych profilu klienta
    class Meta:
        model = Customer
        fields = ["phone_number"]
    def clean_phone_number(self):
        phone = (self.cleaned_data.get("phone_number") or "").strip()
        if phone == "":
            return phone
        if not re.fullmatch(r"\d{9}", phone):
            raise forms.ValidationError("Numer telefonu musi składać się z 9 cyfr.")
        return phone