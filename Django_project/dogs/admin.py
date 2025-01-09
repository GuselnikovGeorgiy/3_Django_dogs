from django.contrib import admin

from dogs.models import Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass
