from rest_framework.views import APIView
from ..models.custom_user import CustomUser
from ..serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response


class LoginView(APIView):
  def post(self, request):
    try:
        data = request.data
        serializer = LoginSerializer(data=data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = CustomUser.objects.filter(email=email).first()
            
            if user is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            valid_password = check_password(serializer.validated_data.get('password'), user.password)
            
            if valid_password:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": "An error occurred. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)