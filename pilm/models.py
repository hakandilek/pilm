from django.utils.translation import ugettext_lazy as _
from django.db import models

class Movie(models.Model):
	key = models.AutoField(primary_key=True)
	imdbId = models.CharField(max_length=31, unique=True)
	title = models.CharField(max_length=255)
	year = models.IntegerField()
	kind = models.CharField(max_length=63)
	rating = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	
	def __unicode__(self):
		return "%s (%s)" % (self.title, self.year)
	
class Pack(models.Model):
	QUERY_STATUS = (
		('N', _('new')),
		('I', _('in progress')),
		('P', _('processed')),
		('A', _('assigned')),
	)
	key = models.AutoField(primary_key=True)
	name = models.CharField(max_length=1023)
	createDate = models.DateTimeField(auto_now_add=True, blank=False)
	updateDate = models.DateTimeField(auto_now=True, blank=False)
	query=models.CharField(max_length=255)
	queryStatus = models.CharField(max_length=12, choices=QUERY_STATUS, default='N', blank=False)
	queryDate = models.DateTimeField(auto_now=True, blank=False)
	movies=models.ManyToManyField(Movie, related_name="movies")
	assignedMovie=models.ForeignKey(Movie, blank=True, null=True, on_delete=models.SET_NULL)#TODO:on delete:set queryStatus=N
	def get_only_movies(self):
		return self.movies.filter(kind='movie').order_by("year")
	
	def __unicode__(self):
		if self.name:
			return self.name
		else:
			return self.query

class File(models.Model):
	key = models.AutoField(primary_key=True)
	name = models.CharField(max_length=1023)
	pack = models.ForeignKey(Pack)
	def __unicode__(self):
		return self.name
