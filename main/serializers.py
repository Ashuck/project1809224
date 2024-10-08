from typing import Any
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from main.models import UserInfo, RedBookSpecies, HabitatAreas, TypeSpecies, SpeciesGallery, UserGallery


class FavoriteSpeciesSerializer(ModelSerializer):
    photo = SerializerMethodField()
    class Meta:
        model = RedBookSpecies
        fields = 'id', 'title', 'photo'
    
    def get_photo(self, obj: RedBookSpecies):
        return obj.main_photo.url


class HabitatAreaSerializer(ModelSerializer):
    class Meta:
        model = HabitatAreas
        fields = 'id', 'title', 'description', 'kadastr'


class DetailHabitatAreaSerializer(ModelSerializer):
    species = SerializerMethodField()

    class Meta:
        model = HabitatAreas
        fields = 'id', 'title', 'description', 'iframe_map', 'species', 'kadastr'
    
    def get_species(self, obj: HabitatAreas):
        return ShortRedBookSpeciesSerializer(obj.red_book_species.all(), many=True).data



class TypeSpeciesSerializer(ModelSerializer):
    description = SerializerMethodField()
    photo = SerializerMethodField()
    class Meta:
        model = TypeSpecies
        fields = 'id', 'title', 'description', "short_description", "photo"
    
    def get_description(self, obj: TypeSpecies):
        return obj.description.split('\n')
    
    def get_photo(self, obj: TypeSpecies):
        return obj.photo.url


class SpeciesGallerySerializer(ModelSerializer):
    photo = SerializerMethodField()
    class Meta:
        model = SpeciesGallery
        fields = 'id', 'photo', 'autor'
    
    def get_photo(self, obj: RedBookSpecies):
        return obj.main_photo.url
    

class RedBookSpeciesSerializer(ModelSerializer):
    photo = SerializerMethodField()
    habitat_area = HabitatAreaSerializer(many=True)
    type = TypeSpeciesSerializer()
    favorite_count = SerializerMethodField()
    is_favorite = SerializerMethodField()
    gallery = SpeciesGallerySerializer(many=True)
    squad = SerializerMethodField()
    family = SerializerMethodField()

    class Meta:
        model = RedBookSpecies
        fields = (
            'id', 'title', 'photo', "type", "status", "spreading",
            'international_name', 'squad', 'family', "additional_info",
            "pop_count", "habitat_features", "limit_features",
            "protect_step", "state_change", "necessary_measures",
            "sources", "autor", "iframe_map", "habitat_area", 
            "favorite_count", "is_favorite", "gallery", "actual_date",
        )
    
    def __init__(self, *args: Any, is_favorite=False, **kwds: Any) -> Any:
        self.is_favorite = is_favorite
        return super().__init__(*args, **kwds)
    
    def get_photo(self, obj: RedBookSpecies):
        return obj.main_photo.url
    
    def get_description(self, obj: RedBookSpecies):
        return obj.description.split('\n')

    def get_favorite_count(self, obj: RedBookSpecies):
        return obj.user_favorities.count()

    def get_is_favorite(self, obj: RedBookSpecies):
        return self.is_favorite
    
    def get_squad(self, obj: RedBookSpecies):
        if not obj.squad: return None
        return f"{obj.squad.title} - {obj.squad.international_name}"

    def get_family(self, obj: RedBookSpecies):
        if not obj.family: return None
        return f"{obj.family.title} - {obj.family.international_name}"

    

class ShortRedBookSpeciesSerializer(ModelSerializer):
    photo = SerializerMethodField()
    is_favorite = SerializerMethodField()

    class Meta:
        model = RedBookSpecies
        fields = 'id', 'title', 'photo', 'is_favorite'

    def __init__(self, *args: Any, is_favorite=False, **kwds: Any) -> Any:
        self.is_favorite = is_favorite
        return super().__init__(*args, **kwds)

    def get_photo(self, obj: RedBookSpecies):
        return obj.main_photo.url

    def get_is_favorite(self, obj: RedBookSpecies):
        return self.is_favorite


class UserGallerySerializer(ModelSerializer):
    specie = ShortRedBookSpeciesSerializer(is_favorite=True)

    class Meta:
        model = UserGallery
        fields = 'id', 'status', 'specie', 'photo'


class UserInfoSerializer(ModelSerializer):
    favorites = SerializerMethodField()
    photo = SerializerMethodField()
    user_gallery = UserGallerySerializer(many=True)

    class Meta:
        model = UserInfo
        fields = 'first_name', 'second_name', 'email', 'id', 'favorites', 'role', 'photo', 'user_gallery'

    def get_favorites(self, obj: UserInfo):
        return FavoriteSpeciesSerializer(obj.favorite_species.all(), many=True).data
    
    def get_photo(self, obj: UserInfo):
        if obj.avatar: return obj.avatar.url
        return None