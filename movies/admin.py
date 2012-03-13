from movies.models import Movie, Scene
from django.contrib import admin

class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Movie, MovieAdmin)
admin.site.register(Scene)
