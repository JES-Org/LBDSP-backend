from django.db import models
from django.conf import settings

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    pharmacy = models.ForeignKey("pharmacy.Pharmacy", on_delete=models.CASCADE, related_name="subscribers")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "pharmacy")  # Prevent duplicate subscriptions
        ordering = ["-subscribed_at"]

    def __str__(self):
        return f"{self.user.email} subscribed to {self.pharmacy.name}"
