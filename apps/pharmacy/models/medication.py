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
    batch_number = models.CharField(max_length=20,blank=True)
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
    def save(self, *args, **kwargs):
        if self.quantity_available == 0:
            self.stock_status = False
        else:
            self.stock_status = True
        if not self.batch_number:
            self.batch_number = f"{self.name[:3].upper()}-{self.pharmacy.name[:3]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.manufacturer} - {self.expiry_date}"
   
    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()
    class Meta:
        unique_together = ('name', 'manufacturer', 'expiry_date')  # Ensures each batch is unique

