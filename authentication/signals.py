from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from core.models import UserInvitation
from surveyor.models import Surveyor
from respondent.models import Respondent


# @receiver(user_signed_up)
# def user_signed_up(request, user, **kwargs):
#     try:
#         invite = UserInvitation.objects.get(email=user.email)
#         user.save()
#     except UserInvitation.DoesNotExist:
#         pass

@receiver(pre_social_login)
def pre_social_login(request, sociallogin, **kwargs):
    user = sociallogin.account.user
    # New user signing up
    if not (Surveyor.objects.filter(user=user).exists() or Respondent.objects.filter(user=user).exists()):
        if UserInvitation.objects.filter(email=user.email).exists():
            invite =  UserInvitation.objects.get(email=user.email)
            if invite.is_respondent:
                group = invite.group
                respondent = Respondent(
                    user=user,
                    firstname=user.first_name,
                    surname=user.last_name
                )
                respondent.save()
                group_respondent = GroupRespondent(
                    group=group,
                    respondent=respondent
                )
                group_respondent.save()
            else:
                organisation = invite.organisation
                surveyor = Surveyor(
                    user=user,
                    firstname=user.first_name,
                    surname=user.last_name,
                    organisation=organisation
                )
                surveyor.save()
    # TODO: need to handle case of organisation admin signing up with social account