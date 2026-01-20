from rest_framework.generics import (GenericAPIView, CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from accounts.models import User, PasswordResetCode
from .serializers import (RegisterSerializer,
                          LoginSerializer,
                          ProfileSerializer,
                          DeactivateAccountSerializer,
                          GenericChangePasswordSerializer,
                          ResetPasswordConfirmSerializer,
                          ResetPasswordRequestSerializer,
                          ResetPasswordVerifySerializer,
                          EmptySerializer
                          )
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    

class ProfileView(RetrieveAPIView, UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
    

class ChangePasswordView(GenericAPIView):
    serializer_class = GenericChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=200)
    

class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Successfully logged out"}, status=204)
    

class DeactivateAccountView(DestroyAPIView):
    serializer_class = DeactivateAccountSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data['confirm']:
            return Response({"detail": "Account deactivation not confirmed"}, status=400)
        
        request.user.is_active = False
        request.user.save()

        return Response({"detail": "Account deactivated successfully"}, status=200)
    

class ResetPasswordRequestView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        email = serializer.validated_data.get('email', None)

        if not email:
            return Response({"message":"Необходимо указать email"}, status=400)
        
        if email and not User.objects.filter(email=email).exists():
            return Response({"message":" Пользователь с таким именем не найден"}, status=400)
        
        from random import randint

        code = str(randint(1000, 9999))
        PasswordResetCode.create_code(email=email)


        message = f"Ваш код для сброса пароля: {code}"


        response = send_mail(
            subject="Востановление пароля",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        if response == 0:
            return Response({"message":"Неудалось отправить код на email"}, status=500)
        return Response({"message":"Код успешно отправлен на email"}, status=200)



class ResetPasswordVerifyView(GenericAPIView):
    serializer_class = ResetPasswordVerifySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data.get('email', None)
        code = serializer.validated_data['code']

        try:
            if email:
                code_record = PasswordResetCode.objects.get(email=email, code=code)
            else:
                return Response({"message":"Необходимо указать email"}, status=400)
            
            if code_record.is_expired():
                code_record.delete()
                return Response({"message":"Срок действий кода истек"}, status=400)
            return Response({"message":"Код успешно проверен"}, status=200)
        
        except PasswordResetCode.DoesNotExist:
            return Response({"message":"Неверный код"}, status=400)



class ResetPasswordConfirmView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data.get('email', None)
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        try:
            if email:
                code_record = PasswordResetCode.objects.get(email=email, code=code)
                user = User.objects.get(email=email)
            else:
                return Response({"message":"Необходимо указать email"}, status=400)
            
            if code_record.is_expired():
                code_record.delete()
                return Response({"message":"Срок действий кода истек"}, status=400)

            user.set_password(new_password)
            user.save()
            code_record.delete()

            return Response({"message":"Код успешно проверен"}, status=200)
        
        except PasswordResetCode.DoesNotExist:
            return Response({"message":"Неверный код"}, status=400)
        
        except User.DoesNotExist:
            return Response({"message":"Пользователь не найден"}, status=400)


