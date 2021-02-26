from django.contrib import admin
from .models import Organisation, SurveyorOrganisation


class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class SurveyorOrganisationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(SurveyorOrganisation, SurveyorOrganisationAdmin)
