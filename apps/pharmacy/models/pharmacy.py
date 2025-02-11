from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    website = models.URLField(null=True, blank=True)
    operating_hours = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='pharmacies/', blank=True, null=True)
    delivery_available = models.BooleanField(default=False)
    latitude = models.FloatField(default= 11.5742)
    longitude = models.FloatField(default=37.3614)
    status = models.CharField(max_length=20, default='Pending')
    def save(self, *args, **kwargs):
        # Automatically update is_verified based on status
        self.is_verified = self.status == "Approved"
        super().save(*args, **kwargs)

  
    def __str__(self):
        return self.name
    
