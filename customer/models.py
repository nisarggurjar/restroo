from django.db import models
from django.contrib.auth.models import User
from management.models import Dish

class Add_to_cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE,blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    confirm = models.BooleanField(blank=True, null=True, default=False)
    
    def __str__(self): 
        return self.user.username + ' <---> ' + self.dish.title
    
class reservation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    guests = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length = 10)
    mob = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    confirm = models.BooleanField(blank=True, null=True, default=False)
    
    def __str__(self):
        return self.name + '<--->' + str(self.date) + '<--->' + str(self.time)
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    HouseNum = models.CharField(max_length=15,blank=True, null=True)
    area = models.CharField(blank=True, null=True, max_length = 50)
    landmark = models.CharField(blank=True, null=True, max_length =50)
    district = models.CharField(blank=True, null=True, max_length = 50)
    city = models.CharField(blank=True, null=True, max_length = 50)
    state = models.CharField(blank=True, null=True, max_length = 50)
    pin = models.IntegerField(blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class user_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    mob = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Payment_ids(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    ids = models.CharField(max_length=100,null=True)