from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from .models import User,Profile
from .serializers import UserRegistationSerialiser,UserLoginSerializer,UserPasswordChangeSerializer,PasswordResetByEmailSerializer,UserPasswordRsetSerializer,ProfileSerializer
from .renderers import UserRenderer


#manually create a token 
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    serializer_class = UserRegistationSerialiser
    def post(self,request,format=None):
        serializer=UserRegistationSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration succesfully compleate'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, formate=None):
        return Response("serializer.errors,status=status.HTTP_400_BAD_REQUEST")


class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    serializer_class = UserLoginSerializer
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login succesfull!'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'Non_field errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#For User Accoount Password Change 
class UserPasswordChangeView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    serializer_class = UserPasswordChangeSerializer
    def post(self,request,format=None):
        serializer=UserPasswordChangeSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password change succesfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PasswordResetByEmailView(APIView):
    renderer_classes=[UserRenderer]
    serializer_class = PasswordResetByEmailSerializer
    def post(self,request,format=None):
        serializer=PasswordResetByEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link send.Please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    serializer_class = UserPasswordRsetSerializer
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordRsetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset succesfull!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




 

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(instance=profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        print(profile.user)
        serializer = ProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)






