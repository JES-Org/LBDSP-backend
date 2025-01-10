from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Medication(models.Model):
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_status = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    dosage_form = models.CharField(max_length=50, choices=[
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
    ])
    dosage_strength = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=100)
    expiry_date = models.DateField()
    prescription_required = models.BooleanField(default=False)
    side_effects = models.TextField(blank=True, null=True)
    usage_instructions = models.TextField(blank=True, null=True)
    quantity_available = models.IntegerField(default=0)
    image = models.ImageField(upload_to='medications/', blank=True, null=True)

    def __str__(self):
        return self.name

    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()
