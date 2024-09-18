from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from main.models import UserInfo, RedBookSpecies
from main.serializers import UserInfoSerializer

# Create your views here.
TokenAuthentication.keyword = "Bearer"

class UserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    

    def get(self, req: Request):
        if req.query_params.get('user_id'):
            
            user_info = UserInfo.objects.filter(pk=req.query_params.get('user_id')).first()
        elif req.user.is_authenticated:
            user_info = req.user.user_info
        else:
            return Response({"description": "No user id or auth"}, status=401)

        return Response({
            "user_info": UserInfoSerializer(user_info).data
        })


class UserRegistrtionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, req: Request):
        email = req.data.get('email')
        username = email
        password = req.data.get('password')

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user_info = UserInfo.objects.create(
                email=email,
                user=user,
                second_name=req.data.get('second_name'),
                first_name=req.data.get('first_name'),
                avatar=req.data.get('avatar')
            )
            token = Token.objects.create(user=user)
        else:
            return Response({"description": "User already exists"}, status=400)

        return Response({
            "user_info": UserInfoSerializer(user_info).data,
            "token": token.key
        })


class UserLoginView(APIView):
    def post(self, req: Request):
        username = req.data.get('username')
        password = req.data.get('password')

        user = User.objects.get(username=username)
        if user.check_password(password):
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response({
                "user_info": UserInfoSerializer(user.user_info).data,
                "token": token.key
            })
        else:
            return Response({"description": "Wrong password"}, status=401)