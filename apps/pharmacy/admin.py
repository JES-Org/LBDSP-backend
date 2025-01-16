from django.contrib import admin

# Register your models here.
from .models.pharmacy import Pharmacy
from .models.medication import Medication, Category
from .models.pharmacist import Pharmacist

admin.site.register(Pharmacy)
admin.site.register(Medication)
admin.site.register(Category)
admin.site.register(Pharmacist)