from django.db import models

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


from django.core.validators import MinValueValidator, MaxValueValidator

class CoffeeTaste(models.Model):
    """Model reprezentujący smak kawy."""
    name = models.CharField(max_length=50)
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
        return f"{self.name}, {self.country}"


class Coffee(models.Model):
    """Model reprezentujący kawę w sklepie."""
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=COFFEE_TYPES, default="Z")
    taste = models.ForeignKey(CoffeeTaste, null=True, blank=True, on_delete=models.SET_NULL)
    producent = models.ForeignKey(Producent, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(
        max_digits=5, #maksymalnie 5 cyfr
        decimal_places=2, #2 miejsca po przecinku
        help_text="Cena kawy w PLN."
    )

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    """Model reprezentujący klienta sklepu."""
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True, editable = False) 
    loyalty_points = models.PositiveIntegerField(
        default=0,
        help_text="Aktualna liczba punktów lojalnościowych klienta."
    )

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    class Meta:
        ordering = ["surname"] #sortuj alfabetycznie po nazwisku


class Order(models.Model):
    """Model reprezentujący zamówienie klienta."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, help_text="Klient, który złożył zamówienie.")
    date_ordered = models.DateTimeField(auto_now_add=True) #automatyczna data złożenia zamówienia
    is_completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        customer_surname = self.customer.surname
        return f'Zamówienie nr {self.id} dla {customer_surname}'

    class Meta:
        ordering = ['-date_ordered'] #sortuj według najnowszego zamówienia


