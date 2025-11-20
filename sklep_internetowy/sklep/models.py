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

    def __str__(self):
        return self.name


