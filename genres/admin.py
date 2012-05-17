from genres.models import Genre
from django.contrib import admin

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("shortDescription",)}

admin.site.register(Genre, GenreAdmin)
