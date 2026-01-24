from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

# Lista wyboru rodzaju kawy
COFFEE_TYPES = (
    ('Z', 'Ziarnista'),
    ('M', 'Mielona'),
    ('K', 'Kapsułki'),
)


# Lista wyboru kraju pochodzenia kawy
COUNTRY = (
    ('BR', 'BRAZYLIA'),
    ('VN', 'WIETNAM'),
    ('CO', 'KOLUMBIA'),
    ('ET', 'ETIOPIA'),
    ('ID', 'INDONEZJA'),
    ('UG', 'UGANDA')
)


class CoffeeTaste(models.Model):
    """Model reprezentujący smak kawy."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, help_text="Krótki opis kawy.")
    coffee_strength = models.IntegerField(
        help_text="Moc kawy w skali od 1-5.",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    coffee_acidity = models.IntegerField(
        help_text="Kwasowość kawy w skali od 1-3.",
        validators=[MinValueValidator(1), MaxValueValidator(3)] 
    )

    def __str__(self):
        return self.name


class Producent(models.Model):
    """Model reprezentujący producenta kawy."""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY)

    def __str__(self):
        return f"{self.name}, {self.get_country_display()}" #Zwracana jest nazwa producenta i pełna nazwa kraju


class Coffee(models.Model):
    """Model reprezentujący kawę w sklepie."""
    name = models.CharField(max_length=100)
    coffeetype = models.CharField(max_length=1, choices=COFFEE_TYPES, default="Z")
    taste = models.ForeignKey(CoffeeTaste, null=True, blank=True, on_delete=models.SET_NULL)
    producent = models.ForeignKey(Producent, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(
        max_digits=5, #maksymalnie 5 cyfr
        decimal_places=2, #2 miejsca po przecinku
        validators=[MinValueValidator(0.01)],#cena minimalna 0.01
        help_text="Cena kawy w PLN."
    )

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    """Profil klienta sklepu powiązany z kontem użytkownika. Klient musi być zalogowany."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=15, blank=True) 
    registration_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        full_name = self.user.get_full_name().strip()
        return full_name if full_name else self.user.username

    class Meta:
        ordering = ["user__last_name", "user__first_name"] #Sortowanie według nazwiska i imienia użytkownika


class Order(models.Model):
    """Zamówienie klienta (tylko zalogowani)."""
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, #nie pozwala usunąć klienta, jeśli ma zamówienia
        related_name="orders", help_text="Klient, który złożył zamówienie.")
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Zamówienie nr {self.id} dla {self.customer.user.get_full_name() or self.customer.user.username}"

    class Meta:
        ordering = ["-date_ordered"] #najnowsze zamówienia pierwsze

class OrderItem(models.Model):
    """Pozycja w zamówieniu."""
    coffee = models.ForeignKey("Coffee", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_order = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Cena kawy w momencie złożenia zamówienia."
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        coffee_name = self.coffee.name if self.coffee else "Usunięty produkt"
        return f"{self.quantity} x {coffee_name} (zamówienie #{self.order.id})"

    @property #Oblicza łączną cenę pozycji w zamówieniu
    def total_price(self):
        return self.quantity * self.price_at_order