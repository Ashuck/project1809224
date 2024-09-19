from collections.abc import Callable, Sequence
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

from main import models


admin.site.register(models.Squads)
admin.site.register(models.Families)
admin.site.register(models.TypeSpecies)


class Inline_SpeciesGallery(admin.StackedInline):
    model = models.SpeciesGallery
    extra = 0
    fields = 'photo', 'autor', 'view_photo'
    readonly_fields = ('view_photo', )

    @admin.display(description='Фотография')
    def view_photo(self, sg:models.SpeciesGallery):
        if sg.photo: content = mark_safe(f'<a href="{sg.photo.url}"><img width="150" height="150" src="{sg.photo.url}"></a>')
        else: content = '-'
        return content


@admin.register(models.RedBookSpecies)
class RedBookSpeciesAdmin(admin.ModelAdmin):
    list_filter = (
        ('type__title',  DropdownFilter),
        ('squad__title',  DropdownFilter),
        ('family__title',  DropdownFilter),
    )
    search_fields = ('title', 'international_name')
    inlines = [Inline_SpeciesGallery]
    readonly_fields = 'map',
    list_display = ('title','type', 'squad', 'family', 'iframe_map_exists', 'actual_date')

    @admin.display(description='Есть карта')
    def iframe_map_exists(self, ub:models.RedBookSpecies):
        if ub.iframe_map != "-": return "+"
        return "-"
    
    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        fields = super().get_fields(request, obj)
        if 'map' in fields: fields.remove('map')
        map_index = fields.index('iframe_map')
        if map_index != -1: fields.insert(map_index + 1, 'map')
        return fields
    
    @admin.display(description='Карта')
    def map(self, ub:models.RedBookSpecies):
        return mark_safe(ub.iframe_map)


class Inline_UserGallery(admin.StackedInline):
    model = models.UserGallery
    extra = 0
    fields = 'specie', 'status', 'photo', 'view_photo'
    readonly_fields = ('view_photo',)
    
    @admin.display(description='Фотография')
    def view_photo(self, ug:models.UserGallery):
        if ug.photo: content = mark_safe(f'<a href="{ug.photo.url}"><img width="150" height="150" src="{ug.photo.url}"></a>')
        else: content = '-'
        return content
    

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_filter = (
        ('role', DropdownFilter),
    )
    list_display = ('first_name', 'second_name', 'role', 'user')
    inlines = [Inline_UserGallery]
    

@admin.register(models.UserGallery)
class UserGalleryAdmin(admin.ModelAdmin):
    list_filter = (
        ('status', DropdownFilter),
        ('user__user__username', DropdownFilter),
    )
    list_display = ('specie','status', 'user')

@admin.register(models.HabitatAreas)
class HabitatAreasAdmin(admin.ModelAdmin):
    pass
    fields = ('title', 'description', 'iframe_map', 'map', 'specie_list')
    readonly_fields = ('map', 'specie_list')

    @admin.display(description='Обитатели')
    def specie_list(self, ha:models.HabitatAreas):
        template = "<div>{}</div>"
        template_element = "<a href=\"{url}\">{title}</a><br>"
        content = ""
        for specie in ha.red_book_species.all():
            content = content + template_element.format(
                url=f"/admin/main/redbookspecies/{specie.id}/change/",
                title=specie.title
            )
        content = template.format(content)
        return mark_safe(content)
    
    @admin.display(description='Карта')
    def map(self, ub:models.RedBookSpecies):
        return mark_safe(ub.iframe_map)

