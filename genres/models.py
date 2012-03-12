from django.db import models

class Genre(models.Model):
    shortDescription = models.CharField(max_length=50)
    longDescription  = models.TextField(blank=True, null=True)
    scenes           = models.ManyToManyField('movies.Scene', blank=True, null=True)
    movies           = models.ManyToManyField('movies.Movie', blank=True, null=True)

    def __unicode__(self):
        return self.shortDescription
