from django.db import models

# Create your models here.
class All_Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True)
    fullname = models.CharField(max_length=100, null=True)
    product = models.CharField(max_length=100, null=True)
    review = models.CharField(max_length=10000, null=True)
    rating = models.IntegerField(null=True)
    label = models.CharField(max_length=10, null=True)
    
    class Meta:
        managed = False
        db_table = 'all_reviews'


class Negative_Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True)
    fullname = models.CharField(max_length=100, null=True)
    product = models.CharField(max_length=100, null=True)
    review = models.CharField(max_length=10000, null=True)
    rating = models.IntegerField(null=True)
    label = models.CharField(max_length=10, null=True)
    
    class Meta:
        managed = False
        db_table = 'negative_reviews'