from django.contrib import admin

# Register your models here.
from .models.pharmacy import Pharmacy
from .models.medication import Medication, Category

admin.site.register(Pharmacy)
admin.site.register(Medication)
admin.site.register(Category)