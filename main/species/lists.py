from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count


from main.models import RedBookSpecies, TypeSpecies, HabitatAreas
from main.serializers import TypeSpeciesSerializer, ShortRedBookSpeciesSerializer, HabitatAreaSerializer

# Create your views here.
TokenAuthentication.keyword = "Bearer"

class SpeciesListView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, req: Request):
        species = RedBookSpecies.objects.all()

        if req.query_params.get('type'):
            tepe_species = TypeSpecies.objects.get(pk=req.query_params.get('type'))
            species = species.filter(type=tepe_species)
        
        if req.query_params.get('habitat_area_id'):
            habitat_areas = HabitatAreas.objects.filter(id=req.query_params.get('habitat_area_id'))
            species = species.filter(habitat_areas__in=habitat_areas)
        
        if req.user.is_authenticated:
            species_fav = species.filter(user_favorities__in=[req.user.user_info])
            species_not_fav = species.exclude(user_favorities__in=[req.user.user_info])
            species_fav = ShortRedBookSpeciesSerializer(species_fav, is_favorite=True, many=True).data
            species_not_fav = ShortRedBookSpeciesSerializer(species_not_fav, many=True).data
            species = species_fav + species_not_fav
        else:
            species = ShortRedBookSpeciesSerializer(species, many=True).data

        return Response({"species": species})


class SpeciesTypesListView(APIView):
    def get(self, req: Request):
        types = TypeSpecies.objects.all()
        return Response({"types": TypeSpeciesSerializer(types, many=True).data})


class HabitatAreasListView(APIView):
    def get(self, req: Request):
        habitat_areas = HabitatAreas.objects.all()
        return Response({"habitat_areas": HabitatAreaSerializer(habitat_areas, many=True).data})
    

class FavoriteSpeciesListView(APIView):
    def get(self, req: Request):
        top_species = RedBookSpecies.objects.annotate(
            count=Count('user_favorities')
        ).order_by('-count')[:3]
        return Response({"top_species": ShortRedBookSpeciesSerializer(top_species, many=True).data})

