from django.urls import path, include
from .views import LogoutView, RegisterView, VerifyuserView, SendVerifycationAgainView, LoginView, CustomTokenRefreshView, ForgotPasswordView, ResetPasswordView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/', VerifyuserView.as_view()),
    path('sendverifyagain/', SendVerifycationAgainView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view())
]