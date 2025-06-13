from django.contrib import admin

# Register your models here.
from .models.pharmacy import Pharmacy
from .models.medication import Medication, Category
from .models.pharmacist import Pharmacist
from .models.review import Review
from .models.searchHistory import SearchHistory


admin.site.register(Medication)
admin.site.register(Category)
admin.site.register(Pharmacist)
admin.site.register(Review)
admin.site.register(SearchHistory)

class PharmacyAdmin(admin.ModelAdmin):
    model = Pharmacy
    list_display = ('id', 'name', 'email', 'address',  'is_verified',
)
    

# Register the Pharmacy model with the custom admin interface
admin.site.register(Pharmacy, PharmacyAdmin)