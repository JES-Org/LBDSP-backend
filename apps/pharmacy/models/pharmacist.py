from django.db import models
from django.conf import settings

class Pharmacist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile"
    )
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    license_image = models.ImageField(upload_to="licenses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.license_number}"