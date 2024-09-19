from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from main.models import RedBookSpecies, HabitatAreas
from main.serializers import TypeSpeciesSerializer, RedBookSpeciesSerializer, DetailHabitatAreaSerializer


class DetailSpeciesView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, req: Request):
        specie = RedBookSpecies.objects.get(pk=req.query_params.get('id'))

        if req.user.is_authenticated and req.user.user_info.favorite_species.filter(pk=specie.pk).exists():
            specie = RedBookSpeciesSerializer(specie, is_favorite=True).data
        else:
            specie = RedBookSpeciesSerializer(specie).data
        return Response(specie)


class UserFavoritesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request):
        specie = RedBookSpecies.objects.get(pk=req.data.get('specie_id')) if req.data.get('specie_id') else None
        if specie:
            req.user.user_info.favorite_species.add(specie)
            return Response({"description": "ok"})
        else:
            return Response({"description": "No such specie"}, status=400)

    def delete(self, req: Request):
        specie = RedBookSpecies.objects.get(pk=req.data.get('specie_id')) if req.data.get('specie_id') else None
        if specie:
            req.user.user_info.favorite_species.remove(specie)
            return Response({"description": "ok"})
        else:
            return Response({"description": "No such specie"}, status=400)


class HabitatAreasDetailView(APIView):
    def get(self, req: Request):
        try:
            habitat_area = HabitatAreas.objects.get(pk=req.query_params.get('area_id'))
        except:
            return Response({"description": "No such area"}, status=404)

        return Response({"habitat_area": DetailHabitatAreaSerializer(habitat_area).data})
