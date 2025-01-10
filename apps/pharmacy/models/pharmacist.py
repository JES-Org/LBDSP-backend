from django.db import models
from django.conf import settings

class Pharmacist(models.Model):
    user = models.OneToOneField(
        settings.Auth_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile"
    )
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE)