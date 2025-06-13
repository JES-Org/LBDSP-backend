from django.db import models

class Notification(models.Model):
    ROLE_CHOICES = [
        ("admin", "admin"), 
        ("pharmacist", "pharmacist"),
        ("user", "user"),
    ]

    notify = models.CharField(max_length=10, choices=ROLE_CHOICES)
    title = models.CharField(max_length=255)
    message=models.CharField(max_length=255)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.title
