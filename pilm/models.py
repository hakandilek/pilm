from django.db import models

class Movie(models.Model):
	name=models.CharField(max_length=255)
	def __unicode__(self):
		return self.name
	
class Pack(models.Model):
	filename=models.CharField(max_length=1023)
	query=models.CharField(max_length=255)
	movies=models.ManyToManyField(Movie)

class File(models.Model):
	name=models.CharField(max_length=1023)
	def __unicode__(self):
		return self.name

