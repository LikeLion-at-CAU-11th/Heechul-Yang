from django.shortcuts import render
from .serializers import ResisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework_simplejwt.serializers import RefreshToken

# Create your views here.

class RegisterView(APIView):
    serializer_class = ResisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            member = serializer.save(request)
            token = RefreshToken.for_user(member)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            res = Response(
                {
                    "member" : serializer.data,
                    "message" : "register success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status= status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)