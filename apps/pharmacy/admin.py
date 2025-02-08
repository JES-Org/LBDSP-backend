from django.contrib import admin

# Register your models here.
from .models.pharmacy import Pharmacy
from .models.medication import Medication, Category
from .models.pharmacist import Pharmacist
from .models.review import Review
from .models.subscription import Subscription
from .models.notification import Notification

admin.site.register(Pharmacy)
admin.site.register(Medication)
admin.site.register(Category)
admin.site.register(Pharmacist)
admin.site.register(Review)
admin.site.register(Subscription)
admin.site.register(Notification)