from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from apps.pharmacy.models.pharmacist import Pharmacist
from apps.pharmacy.models.pharmacy import Pharmacy

User = get_user_model()

# @receiver(post_save, sender=CustomUser)
# def create_pharmacist_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "pharmacist":
#         Pharmacist.objects.create(user=instance)

# @receiver(post_save, sender=CustomUser)
# def save_pharmacist_profile(sender, instance, **kwargs):
#     if instance.role == "pharmacist" and hasattr(instance, "pharmacist_profile"):
#         instance.pharmacist_profile.save()

@receiver(post_save, sender=Pharmacy)
def notify_admin_on_pharmacy_registration(sender, instance, created, **kwargs):
    if created:
        admin_users = User.objects.filter(is_superuser=True)
        admin_emails = [admin.email for admin in admin_users if admin.email]

        subject = "New Pharmacy Registration"
        message = f"A new pharmacy '{instance.name}' has been registered and is pending approval."

        if admin_emails:
            send_mail(subject, message, settings.EMAIL_HOST_USER, admin_emails)

        pharmacist = Pharmacist.objects.filter(pharmacy=instance).first()
        if pharmacist:
            owner_email = pharmacist.user.email
        
        if owner_email:
            send_mail(
                "Pharmacy Registration Received",
                f"Dear {instance.owner.first_name},\n\nYour pharmacy '{instance.name}' registration has been received. Our team will review it soon.",
                settings.DEFAULT_FROM_EMAIL,
                [instance.owner.email]
            )