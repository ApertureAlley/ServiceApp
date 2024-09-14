from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from ..models.custom_user import CustomUser
from ..serializers import CustomUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()  # Handle OTP validation here
                return Response({'message': 'User created successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def show(self, request):
        serializer = CustomUserSerializer(request.custom_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        if("email" in request.data or "role" in request.data):
            return Response({ 'message': 'Email or Role cannot be updated'}, status=400)
        else:
            serializer = self.get_serializer(request.custom_user, data=request.data, partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)


    def delete(self, request):
        try:
            instance = request.custom_user
            instance.delete()
            return Response({'message': 'User deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def index(self, request):
        current_user = request.custom_user  # Get the currently authenticated user
        users = CustomUser.objects.exclude(id=current_user.id)  # Exclude the current user
        serializer = CustomUserSerializer(users, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data


