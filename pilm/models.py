from django.db import models

class Movie(models.Model):
	name=models.CharField(max_length=255)
	def __unicode__(self):
		return self.name

class Pack(models.Model):
	name=models.CharField(max_length=1023)
	query=models.CharField(max_length=255)
	movies=models.ManyToManyField(Movie)
	def __unicode__(self):
		if self.name:
			return self.name
		else:
			return self.pack_set

class File(models.Model):
	name=models.CharField(max_length=1023)
	pack=models.ForeignKey(Pack, blank=True, null=True, on_delete=models.SET_NULL)
	def __unicode__(self):
		return self.name
