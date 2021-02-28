from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from invitations.signals import invite_accepted
from core.models import UserInvitation
from invitations.utils import get_invitation_model

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    print("SIGNED UP")
    try:
        # Invitation = get_invitation_model() ### Get the Invitation model
        print("Request: " + str(request))
        print("User: " + str(user))
        print("Kwargs: " + str(kwargs))
        invite = UserInvitation.objects.get(email=user.email) ### Grab the Invitation instance
        print("Invite:", invite)
        print("Invite Group:", invite.organisation)
        user.save()
    except UserInvitation.DoesNotExist:
        print("this was probably not an invited user.")