from django.db import models

class Person(models.Model):
    firstName = models.CharField(max_length=100)
    lastName  = models.CharField(max_length=100)
    picture   = models.ImageField(upload_to='images/person/portrait/', blank=True, null=True)
    gender    = models.CharField(max_length=1)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.firstName + " " + self.lastName

class Actor(models.Model):
    person = models.ForeignKey(Person)
    scenes = models.ManyToManyField('movies.Scene', blank=True, null=True)
    movies = models.ManyToManyField('movies.Movie', blank=True, null=True)
    additionalNames = models.TextField(blank=True, null=True)
    measurements = models.CharField(max_length=20, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.person.firstName + " " + self.person.lastName
