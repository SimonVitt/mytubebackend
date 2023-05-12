from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from members.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def send_confirmation_email_register(sender, instance, created, **kwargs):
    if created:
        user = instance
        token = RefreshToken.for_user(user).access_token
        send_mail(
            'Confirm Account',
            f'Hello {user.username}, \n please click on the Link to confirm your account :) \n http://localhost:4200/account-created/{token}',
            'kontakt@simon-vitt.de',
            [user.email],
            fail_silently=False
        )
