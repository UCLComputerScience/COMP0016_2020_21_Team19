from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from core.models import UserInvitation
from surveyor.models import Surveyor, Organisation
from respondent.models import Respondent, GroupRespondent
from urllib.parse import parse_qsl, urlsplit


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    if request.session.get('organisation_name'):
        organisation_name = request.session.pop('organisation_name')
        organisation = Organisation.objects.create(name=organisation_name)
        surveyor = Surveyor(
                user=user,
                firstname=user.first_name,
                surname=user.last_name,
                organisation=organisation
            )
        surveyor.save()
        organisation.admin = surveyor
        organisation.save()
    else:
        try:
            invite = UserInvitation.objects.get(email=user.email)
        except UserInvitation.DoesNotExist:
            pass
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
