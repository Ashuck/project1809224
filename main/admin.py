from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe


from main import models


# admin.site.register(models.UserInfo)
# admin.site.register(models.UserGallery)
admin.site.register(models.Squads)
admin.site.register(models.Families)
admin.site.register(models.HabitatAreas)
admin.site.register(models.TypeSpecies)


class Inline_SpeciesGallery(admin.StackedInline):
    model = models.SpeciesGallery
    extra = 0
    fields = 'photo', 'autor', 'view_photo'
    readonly_fields = ('view_photo', )

    @admin.display(description='Фотография')
    def view_photo(self, sg:models.SpeciesGallery):
        if sg.photo:
            content = mark_safe(
                f'''<a href="{sg.photo.url}">
                <img width="150" height="150" src="{sg.photo.url}">
                </a>''')
        else:
            content = '-'
        return content


@admin.register(models.RedBookSpecies)
class RedBookSpeciesAdmin(admin.ModelAdmin):
    inlines = [Inline_SpeciesGallery]


class Inline_UserGallery(admin.StackedInline):
    model = models.UserGallery
    extra = 0
    fields = 'specie', 'status', 'photo', 'view_photo'
    readonly_fields = ('view_photo',)
    
    @admin.display(description='Фотография')
    def view_photo(self, ug:models.UserGallery):
        if ug.photo:
            content = mark_safe(
                f'''<a href="{ug.photo.url}">
                <img width="150" height="150" src="{ug.photo.url}">
                </a>''')
        else:
            content = '-'
        return content
    

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    inlines = [Inline_UserGallery]

@admin.register(models.UserGallery)
class UserGalleryAdmin(admin.ModelAdmin):
    pass
