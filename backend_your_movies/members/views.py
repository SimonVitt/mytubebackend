from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from members.models import User
from django.core.mail import send_mail
from django.conf import settings
import jwt
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class= RegisterSerializer
    authentication_classes = [] 
    
class VerifyuserView(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        token=request.data['token']
        try:
            payload = jwt.decode(token, settings.SIMPLE_JWT['VERIFYING_KEY'], algorithms=["RS256"])
            user=User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as idetifier:
            return Response({'error': 'Activation expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        
class SendVerifycationAgainView(APIView):
    authentication_classes = [] 
    def post(self, request, *args, **kwargs):
        email=request.data['email']
        try:
            user = User.objects.get(email=email)
            token=RefreshToken.for_user(user).access_token
            send_mail(
                'Confirm Account',
                f'Hello {user.username}, \n please click on the Link to confirm your account :) \n https://mytube.simon-vitt.de/account-created/{token}',
                'kontakt@simon-vitt.de',
                [user.email],
                fail_silently=False
            )
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ForgotPasswordView(APIView):
    authentication_classes = []
    def post(self, request):
        email=request.data['email']
        try:
            user = User.objects.get(email=email)
            token=RefreshToken.for_user(user).access_token
            send_mail(
                'Reset Password',
                f'Hello {user.username}, \n please click on the Link to reset your password :) \n https://mytube.simon-vitt.de/new-password/{token}',
                'kontakt@simon-vitt.de',
                [user.email],
                fail_silently=False
            )
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ResetPasswordView(APIView):
    serializer_class=ResetPasswordSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
       
        return Response(status=status.HTTP_200_OK)
    
        
class LoginView(APIView):
    serializer_class=LoginSerializer
    authentication_classes = []
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = request.data['refresh']
        simple_jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        refresh_token = jwt.decode(request.data['refresh'], simple_jwt_settings.get('VERIFYING_KEY', ''), algorithms=['RS256'])
        current_user = User.objects.get(id=refresh_token['user_id'])
        RefreshToken(request.data['refresh']).blacklist()
        
        return Response({"tokens":current_user.tokens()}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            else:
                return Response({'detail': 'refresh_token parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
