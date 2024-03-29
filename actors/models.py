from django.db import models

class Person(models.Model):
    GenderChoice = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    )

    firstName = models.CharField(max_length=100)
    lastName  = models.CharField(max_length=100)
    picture   = models.ImageField(upload_to='images/person/portrait/', blank=True, null=True)
    gender    = models.CharField(max_length=1, choices=GenderChoice, default='o')
    description = models.CharField(max_length=500, blank=True, null=True)
    alternativeNames = models.TextField(blank=True, null=True)
    birthday  = models.DateField(blank=True, null=True)
    ethnicity = models.CharField(max_length=20, blank=True, null=True)
    detailedInformation = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.firstName + " " + self.lastName

    def getFullName(self):
        return self.firstName + " " + self.lastName

class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person)
    scenes = models.ManyToManyField('movies.Scene', blank=True, null=True)

    @models.permalink
    def getAbsoluteUrl(self):
        return ('detail', (self.id,))

    def __unicode__(self):
        return str(self.id) + ": " + self.person.firstName + " " + self.person.lastName
