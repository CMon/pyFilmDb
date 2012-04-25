from django.db import models

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey('actors.Person')
    movies = models.ManyToManyField('movies.Movie')

    def __unicode__(self):
        return self.person.firstName + " " + self.person.lastName
