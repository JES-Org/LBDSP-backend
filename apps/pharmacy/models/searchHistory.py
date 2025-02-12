
from .medication import Medication
from django.db import models

class SearchHistory(models.Model):
    medication_name = models.CharField(max_length=255,blank=True, default="unknown")
    search_count = models.IntegerField(default=0)
    last_searched = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medication_name} searched {self.search_count} times"

    def increment_search_count(self):
        self.search_count += 1
        self.save()

    @classmethod
    def get_most_searched(cls, limit=5):
        return cls.objects.order_by('-search_count')[:limit]