# models.py

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class AggregatedCategory(models.Model):
    main_category = models.CharField(max_length=250)
    sub_category = models.CharField(max_length=250)

    def __str__(self):
        return self.sub_category

class Product(models.Model):
    no_of_ratings = models.IntegerField(null=True)
    sub_category = models.CharField(max_length=100, null=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ratings = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    name = models.CharField(max_length=255, null=True)
    link = models.URLField(null=True)  
    main_category = models.CharField(max_length=100, null=True)  

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    
def type_to_string(self):
        if self.type == "UN":
            return "Unspecified"
        elif self.type == "TU":
            return "Tutorial"
        elif self.type == "RS":
            return "Research"
        elif self.type == "RW":
            return "Review"

def __str__(self):
    return f"{self.author}: {self.title} ({self.created_datetime.date()})"


