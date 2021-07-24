from django.db import models

# Create your models here.
class Apikey(models.Model):
	username =  models.CharField(max_length = 10)
	apikey =  models.CharField(max_length = 30, default = None)