from django.db import models

# Create your models here.
class NationalStats(models.Model):
	name = models.CharField(max_length=30)
	total_births = models.IntegerField()
	total_cost = models.FloatField()
	total_energy = models.FloatField()
	total_maint = models.FloatField()
	total_req = models.FloatField()
	total_volume = models.FloatField()
	
	def __unicode__(self):
		return self.name