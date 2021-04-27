from .models import User
from .serializers import ChangePasswordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class VerifyEmail(APIView):
    model_class = User
    def get(self, request, pk):
        try:
            user = self.model_class.objects.get(id=pk)
            user.is_verified = True
            user.save()
            
            return Response("Successfully Verified", status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'Not a valid uid'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    model_class      = User

    def post(self, request, pk):
        try:
            user = self.request.data

            for field in ['password', 'confirm_password']:
                if not user.get(field):
                    return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)
                
                if user['password'] != user['confirm_password']:
                    return Response(f"Passwords doesn't match", status.HTTP_400_BAD_REQUEST)
                
                password = self.request.data['password']
                user = self.model_class.objects.filter(id=pk).update(password=password)

                return Response("Passwords Changed Successfully")

        except User.DoesNotExist:
            return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)


