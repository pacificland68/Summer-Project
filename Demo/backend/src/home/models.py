from django.db import models

# Create your models here.
class Property(models.Model):
    listing_id = models.CharField(max_length=21)
    post_town = models.CharField(max_length=100)
    district = models.CharField(max_length=20)
    sector = models.CharField(max_length=20)
    unit1 = models.CharField(max_length=20)
    unit2 = models.CharField(max_length=20)
    property_type = models.CharField(max_length=20)
    last_published_date_day = models.CharField(max_length=20)
    last_published_date_month = models.CharField(max_length=20)
    last_published_date_year = models.CharField(max_length=20)
    num_bathrooms = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_floors = models.IntegerField()
    num_recepts = models.IntegerField()
    price = models.IntegerField()

class Save(models.Model):
    username = models.CharField(max_length=21)
    listing_id = models.CharField(max_length=20)
    outcode = models.CharField(max_length=20)
    property_type = models.CharField(max_length=20)
    first_published_date_day = models.CharField(max_length=20)
    first_published_date_month = models.CharField(max_length=20)
    first_published_date_year = models.CharField(max_length=20)
    last_published_date_day = models.CharField(max_length=20)
    last_published_date_month = models.CharField(max_length=20)
    last_published_date_year = models.CharField(max_length=20)
    num_bathrooms = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_floors = models.IntegerField()
    num_recepts = models.IntegerField()
    price = models.IntegerField()

class recommend(models.Model):
    username = models.CharField(max_length=21)
    recommend = models.CharField(max_length=1000)