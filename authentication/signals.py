from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from core.models import UserInvitation


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    try:
        invite = UserInvitation.objects.get(email=user.email)
        user.save()
    except UserInvitation.DoesNotExist:
        pass
