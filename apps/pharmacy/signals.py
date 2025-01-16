from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import CustomUser
from apps.pharmacy.models.pharmacist import Pharmacist

# @receiver(post_save, sender=CustomUser)
# def create_pharmacist_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "pharmacist":
#         Pharmacist.objects.create(user=instance)

# @receiver(post_save, sender=CustomUser)
# def save_pharmacist_profile(sender, instance, **kwargs):
#     if instance.role == "pharmacist" and hasattr(instance, "pharmacist_profile"):
#         instance.pharmacist_profile.save()