from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=35)
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=35, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    mrp = models.IntegerField(blank=True, null=True)
    img = models.FileField(blank=True, null=True)
    img1 = models.FileField(blank=True, null=True)
    img2 = models.FileField(blank=True, null=True)
    dis = models.TextField(blank=True, null=True)
    avail = models.BooleanField(blank=True, null=True ,default=True)
    
    def __str__(self):
        return self.title + '---' + str(self.cat.name)
    
class Team(models.Model):
    name = models.CharField(blank=True, null=True, max_length = 30)
    designation = models.CharField(blank=True, null=True, max_length = 30)
    img = models.FileField(blank=True, null=True)
    fb = models.URLField(blank=True, null=True)
    tw = models.URLField(blank=True, null=True)
    insta = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

