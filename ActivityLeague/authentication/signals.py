from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from invitations.signals import invite_url_sent, invite_accepted
from invitations.models import Invitation
from invitations.utils import get_invitation_model

# @receiver(invite_accepted)
# def invite_accepted():
#     print("This was run")

@receiver(invite_url_sent, sender=Invitation)
def invite_url_sent(sender, instance, invite_url_sent, inviter, **kwargs):
    Invitation = get_invitation_model()
    invite = Invitation.objects.get(email=user.email)
    print("INVITE URL SENT")
    print(invite)

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    print("SIGNED UP")
    try:
        Invitation = get_invitation_model() ### Get the Invitation model
        invite = Invitation.objects.get(email=user.email) ### Grab the Invitation instance
        user.patient = invite.patient ### Pass your invitation's patient to the related user
        user.save()
    except Invitation.DoesNotExist:
        print("this was probably not an invited user.")