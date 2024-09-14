from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import ServiceProviderProfile
from ..serializers import ServiceProviderProfileSerializer
from rest_framework.viewsets import ModelViewSet

class ServiceProviderProfileModelView(ModelViewSet):
    serializer_class = ServiceProviderProfileSerializer
    queryset = ServiceProviderProfile.objects.all ()

    def create(self, request):
        if not hasattr(request, 'custom_user') or request.custom_user is None:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        custom_user = request.custom_user
        if custom_user.role != 'service_provider':
            return Response({"detail": "User does not have the required role to create a profile."}, status=status.HTTP_403_FORBIDDEN)

        existing_profile = ServiceProviderProfile.objects.filter(user=custom_user).first()
        if existing_profile:
            return Response({"detail": "Profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ServiceProviderProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # User is set in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def show(self, request):
        if not hasattr(request, 'custom_user') or request.custom_user is None:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        custom_user = request.custom_user
        profile = get_object_or_404(ServiceProviderProfile, user=custom_user)
        serializer = ServiceProviderProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    

    def update(self, request):
        if not hasattr(request, 'custom_user') or request.custom_user is None:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile = get_object_or_404(ServiceProviderProfile, user=request.custom_user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        if not hasattr(request, 'custom_user') or request.custom_user is None:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        custom_user = request.custom_user
        profile = get_object_or_404(ServiceProviderProfile, user=custom_user)
        profile.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    def index(self, request):
        current_user = request.custom_user
        users = ServiceProviderProfile.objects
        serializer = ServiceProviderProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

