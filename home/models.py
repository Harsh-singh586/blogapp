from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.
class Page(models.Model):
	username = models.CharField(max_length = 30)
	post_id = models.CharField(max_length = 30)
	headline = models.CharField(max_length = 500)
	reactions = models.IntegerField(default = 0)
	date = models.DateField()
	content = models.TextField()
	category = models.CharField(max_length = 10,default = 'Other')
	img = models.TextField()
	def __str__(self):
		return self.post_id

class Comments(models.Model):
	author = models.CharField(max_length = 30)
	username = models.CharField(max_length = 30)
	post_id = models.CharField(max_length = 30)
	comment_id = models.CharField(max_length = 30,default = None)
	comments = models.CharField(max_length = 100)
	def __str__(self):
		return self.post_id

class Reaction(models.Model):
	author = models.CharField(max_length = 30)
	username = models.CharField(max_length = 30)
	post_id = models.CharField(max_length = 30)
	reaction = models.BooleanField()
	def __str__(self):
		return self.post_id

class Emailverify(models.Model):
	username = models.CharField(max_length = 16)
	activation_key = models.CharField(max_length = 16)

class Forgetpass(models.Model):
	username = models.CharField(max_length = 10)
	verification_key = models.CharField(max_length = 16)

class Stats(models.Model):
	author = models.CharField(max_length = 30)
	post_id = models.CharField(max_length = 30)
	ip = models.CharField(max_length = 30)
	country = models.CharField(max_length = 30)
	region = models.CharField(max_length = 30)
	date = models.DateField()
	time = models.TimeField()
	visitoros = models.CharField(max_length = 30, default = 'other')
	browser = models.CharField(max_length = 30, default = 'other')
