from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .utils import Util
from .serializers import RegisterSerializer, LoginSerializer, ForgetPasswordSerializer, ChangePasswordSerializer
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    model_class      = User

    def post(self, request):
        data = request.data
        serializers = self.serializer_class(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        _data = serializers.data
        uid = _data['id']
        email = _data['email']

        # user = self.model_class.objects.get(email=uid)

        current_site = get_current_site(request).domain
        relativeLink = '/email-verify/'
        absurl = 'http://'+current_site+relativeLink + uid

        email_body = 'Hi user, please use this verification link to verify your account \n' + absurl
        data = {'email_body': email_body, 'to_email': email, 'email_subject': 'Verify your email'}

        Util.send_email(data)

        data = {
            'message': 'Verification link sent to ' + email,
            'data': _data
        }

        return Response(data, status.HTTP_200_OK)

class LoginView(APIView):
    serializer_class = LoginSerializer
    model_class      = User

    def post(self, request):
        user = self.request.data

        try:
            for field in ['email', 'password']:
                if not user.get(field):
                    return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)
            email = self.request.data['email']
            password = self.request.data['password']

            instance = self.model_class.objects.get(email=email)
            serializer = self.serializer_class(instance=instance)
            _data = serializer.data

            if not instance.is_verified:
                return Response(f"User not Verified", status.HTTP_400_BAD_REQUEST)

            if instance.password != password:
                return Response(f"Incorrect Password", status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken.for_user(instance)

            data = {
                'message': 'Login Successfully',
                'access': str(token.access_token)
            }

            return Response(data, status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response('User does not exist', status.HTTP_400_BAD_REQUEST)
            
class ForgetPasswordView(APIView):
    serializer_class = ForgetPasswordSerializer
    model_class      = User

    def post(self, request):
        try:
            if not self.request.data.get('email'):
                return Response(f"Email is required", status=status.HTTP_400_BAD_REQUEST)
            
            email = self.request.data['email']
            instance = self.model_class.objects.get(email=email)

            serializer = self.serializer_class(instance=instance)
            _data = serializer.data

            uid = _data['id']
            email = _data['email']

            current_site = get_current_site(request).domain
            relativeLink = '/change-pass/'
            absurl = 'http://' + current_site + relativeLink + uid

            email_body = 'Hi user, please use this link to change your password, \n' + absurl
            data = {'email_body': email_body,'to_email': email, 'email_subject':'Change your password'}

            Util.send_email(data)
            data = {'uid': uid ,'message': 'Link has been sent to '+ email + ' to change the passeword'}
            return Response(data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

# class UserListing(ListCreateAPIView):
# 	"""docstring for UserListing"""
# 	serializer_class = LoginSerializer
# 	queryset = User.objects.all()
# 	permission_classes = [permissions.IsAuthenticated]