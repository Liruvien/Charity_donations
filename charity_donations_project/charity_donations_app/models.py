from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    
class Institution(models.Model):
    FOUNDATION = 'foundation'
    NGO = 'non-governmental organization'
    LOCAL_COLLECTION = 'local collection'
    TYPE_CHOICES = [
        (FOUNDATION, 'Foundation'),
        (NGO, 'Non-governmental organization'),
        (LOCAL_COLLECTION, 'Local collection'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    type = models.CharField(
        max_length=50, 
        choices=TYPE_CHOICES, 
        default=FOUNDATION
    )
    categories = models.ManyToManyField('Category', related_name='institutions',)

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({dict(self.TYPE_CHOICES).get(self.type, self.type)})"
  

class Donation(models.Model):
    quantity = models.PositiveIntegerField(verbose_name="Quantity of bags")
    categories = models.ManyToManyField('Category', related_name='donations')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name="Street + House number")
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Donation of {self.quantity} bags from {self.user}"
