from django.contrib.auth import authenticate
from django.core.mail import send_mail
from . import models, serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
import random
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
            is_active=False
        )
        code = ''.join([str(random.randint(0, 9) for i in range(6))])
        models.SMSCode.objects.create(user=user, code=code)
        send_mail(
            'Ragistration code',
            message=code,
            from_email='<EMAIL>',
            recipient_list=[user.email],
        )
        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Invalid credentials'})


class SMSCodeConfirm(APIView):
    def post(self, request):
        serializer = serializers.SMSCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        sms_code = serializer.validated_data.get('sms_code')
        try:
            models.SMSCode.objects.get(sms_code=sms_code)
        except models.SMSCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'SMS code not found'})
        sms_code.user.is_active = True
        sms_code.user.save()
        sms_code.delete()
        return Response(status=status.HTTP_200_OK)
