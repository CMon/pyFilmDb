from django.db import models
from actors.models import Actor
from genres.models import Genre

class Movie(models.Model):
    class Meta:
        permissions = (
            ("watch", "Can watch movielist, movie details and scenes"),
            ("allowedRestricted", "Can watch restriced scenes")
        )
    title = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    productionDate = models.DateField(blank=True, null=True)
    frontCover = models.ImageField(upload_to='images/movies/', blank=True, null=True)
    backCover = models.ImageField(upload_to='images/movies/', blank=True, null=True)
    restrictedView = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('detail', (self.slug,))

    def __unicode__(self):
        return self.title

class Scene(models.Model):
    class Meta:
        permissions = (
            ("watch", "Can watch movielist, movie details and scenes"),
            ("allowedRestricted", "Can watch restriced scenes")
        )
    sha256 = models.CharField(max_length=64, null=False, unique=True)
    movie = models.ForeignKey(Movie)
    title = models.CharField(max_length=500)
    animatedImage = models.CharField(max_length=500, blank=True, null=True)
    stillImage = models.CharField(max_length=500, blank=True, null=True)
    sceneRelPath = models.CharField(max_length=500, blank=True, null=True)
    duration = models.IntegerField()
    restrictedView = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.sha256

    def getAllActors(self):
        return Actor.objects.filter(scenes=self)

    def getAllGenres(self):
        return Genre.object.filter(scenes=self)
