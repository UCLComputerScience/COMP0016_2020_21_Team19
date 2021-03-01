from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from invitations.signals import invite_accepted
from core.models import UserInvitation
from invitations.utils import get_invitation_model

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    try:
        # Invitation = get_invitation_model() ### Get the Invitation model
        invite = UserInvitation.objects.get(email=user.email) ### Grab the Invitation instance
        user.save()
    except UserInvitation.DoesNotExist:
        pass