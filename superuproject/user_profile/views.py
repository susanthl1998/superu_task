from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserInfo
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


# Create your views here.

class RegisterApiView(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer

    def send_email(self, req, token):
        current_site = get_current_site(req).domain
        relative_link = reverse('verify_email')
        email = req.data['email']
        url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = "Hi, please click the link below to verify your email\n" + url
        email_data = {'email_body': email_body, 'email_subject': 'Please verify your email', 'to': email}

        Util.send_mail(email_data)
        return req

    def post(self, req):
        data = req.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user)
            access_token = token.access_token
            req = self.send_email(req, access_token)
            message = 'Your account has been successfully created. Please verify your email.'
            response_data = {'user_data': user_data, 'message': message}

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            message = {'error': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailApiView(generics.GenericAPIView):
    def get(self, req):
        token = req.GET.get('token')
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            message = {'message': 'Your email has been verified successfully'}
            return Response(message, status=status.HTTP_200_OK)

        except Exception as e:
            message = {'error': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, req):
        data = req.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserProfileApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserProfileSerializer
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer

    def post(self, req):
        data = req.data
        user_id = req.user.id
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            profile_data = serializer.validated_data
            mobile_number = profile_data['mobile_number']
            user_bio = profile_data['user_bio']
            pincode = profile_data['pincode']
            city = profile_data['city']
            occupation = profile_data['occupation']
            user_info = UserInfo.objects.create(
                mobile_number=mobile_number,
                user_bio=user_bio,
                pincode=pincode,
                city=city,
                occupation=occupation,
                user_id=user_id
            )
            data = {'message': 'Your Profile details has been updated'}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {'error': str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, req):
        data = req.data
        user_id = req.user.id
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            profile_data = serializer.validated_data
            mobile_number = profile_data.get('mobile_number','')
            user_bio = profile_data.get('user_bio', '')
            pincode = profile_data.get('pincode', '')
            city = profile_data.get('city', '')
            occupation = profile_data.get('occupation', '')

            user_info_instance = UserInfo.objects.get(user_id=user_id)
            if mobile_number:
                user_info_instance.mobile_number = mobile_number
            if user_bio:
                user_info_instance.user_bio = user_bio
            if pincode:
                user_info_instance.pincode = pincode
            if city:
                user_info_instance.city = city
            if occupation:
                user_info_instance.occupation = occupation
            user_info_instance.save()
            data = {'message': 'Your Profile details has been updated'}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {'error': str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
