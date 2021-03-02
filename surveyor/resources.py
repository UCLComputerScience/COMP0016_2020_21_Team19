from import_export import resources
from core.models import UserInvitation

class UserInvitationResource(resources.ModelResource):
    class Meta:
        model = UserInvitation
        fields = ['email']

        def after_save_instance(
            self, instance: UserInvitation, using_transactions: bool, dry_run: bool,):
            super().after_save_instance(instance, using_transactions, dry_run)
            if dry_run is False:
                instance.send_invitation()