from django.db import models
from django.utils import timezone

# Create Class for cells of main table
class CellValue(models.Model):
    #author = models.ForeignKey('auth.User')
    #title = models.CharField(max_length=200)
    #text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    site_name = 'MASTER-SAAO'
    
    def  sun_alt(self):
        return '45'

    def __str__(self):
        return self.site_name
