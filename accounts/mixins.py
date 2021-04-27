from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginMixin:
    def post(self, request):
        user = self.request.data

        try:
            for field in ['email', 'password']:
                if not user.get(field):
                    return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)
            email = self.request.data['email']
            password = self.request.data['password']

            instance = self.model_class.objects.get(email=email)
            serializer = self.get_serializer(instance=instance)
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

        except self.model_class.DoesNotExist:
            return Response('User does not exist', status.HTTP_400_BAD_REQUEST)