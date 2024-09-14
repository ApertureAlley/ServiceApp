from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..models import CustomUser, Otp
from ..serializers import CustomUserSerializer, OtpSerializer
import pyotp
from django.core.mail import send_mail
from django.conf import settings

# This can be used for Otp send to User purpose
class OtpViewSet(ModelViewSet):
  serializer_class = OtpSerializer
  queryset = Otp.objects.all()

  def create_otp(self, request):
    otp = pyotp.TOTP('base32secret3232').now()
    recipient_email = request.data.get('email')

    if recipient_email:
      otp_instance, created = Otp.objects.update_or_create(
        email=recipient_email,
        defaults={'code': otp}
      )

      subject = 'OTP Created'
      message = f'Your OTP: {otp}'
      from_email = settings.DEFAULT_FROM_EMAIL  # Ensure this is set in your settings

      try:
        send_mail(subject, message, from_email, [recipient_email])
        return Response({'message': 'OTP created and email sent'}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({'error': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

  def verify_otp(self, request):
    serializer = OtpSerializer(data=request.data)
    if serializer.is_valid():
      email = serializer.validated_data['email']
      code = serializer.validated_data['code']
      try:
        otp_instance = Otp.objects.get(email=email)
        if otp_instance.code == code:
          return Response({'message': 'OTP is valid'}, status=status.HTTP_200_OK)
        else:
          return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
      except Otp.DoesNotExist:
          return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)