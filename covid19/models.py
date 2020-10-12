from django.db import models

# Create your models here.
class censusdata(models.Model):
    managed = True
    geocodeid = models.IntegerField("geographic code identifier",primary_key=True)
    population = models.IntegerField("Population", null=False)
    density = models.FloatField("Population density", null=True)

def __str__(self):
    return self.name