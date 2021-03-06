from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from core.models import UserInvitation
from surveyor.models import Surveyor
from respondent.models import Respondent, GroupRespondent
from urllib.parse import parse_qsl, urlsplit


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    url = request.META.get('HTTP_REFERER')
    params = dict(parse_qsl(urlsplit(url).query))
    if 'org' in params:
        organisation = Organisation.objects.get(id=params['org'])
        surveyor = Surveyor(
                user=user,
                firstname=user.first_name,
                surname=user.last_name,
                organisation=organisation
            )
        surveyor.save()
        organisation.admin = surveyor
        organisation.save()
        return
    else:
        try:
            invite = UserInvitation.objects.get(email=user.email)
        except UserInvitation.DoesNotExist:
            pass # TODO: First Surveyor case / random sign in attempt using SSO from 
        else:
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

# @receiver(pre_social_login)
# def pre_social_login(request, sociallogin, **kwargs):
#     print("ACCOUNT: ", sociallogin.account.__dict__)
#     print("SocialLogin: ", dir(sociallogin))
#     user = sociallogin.account.user
#     # New user signing up
#     if not (Surveyor.objects.filter(user=user).exists() or Respondent.objects.filter(user=user).exists()):
#         if UserInvitation.objects.filter(email=user.email).exists():
#             invite =  UserInvitation.objects.get(email=user.email)
#             if invite.is_respondent:
#                 group = invite.group
#                 respondent = Respondent(
#                     user=user,
#                     firstname=user.first_name,
#                     surname=user.last_name
#                 )
#                 respondent.save()
#                 group_respondent = GroupRespondent(
#                     group=group,
#                     respondent=respondent
#                 )
#                 group_respondent.save()
#             else:
#                 organisation = invite.organisation
#                 surveyor = Surveyor(
#                     user=user,
#                     firstname=user.first_name,
#                     surname=user.last_name,
#                     organisation=organisation
#                 )
#                 surveyor.save()
#     # TODO: need to handle case of organisation admin signing up with social account
