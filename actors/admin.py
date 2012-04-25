from actors.models import Actor, Person
from django.contrib import admin

class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("id",)}

admin.site.register(Actor, ActorAdmin)
admin.site.register(Person)
