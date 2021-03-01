from django.contrib import admin
from .models import Respondent, Response, GroupRespondent

class GroupRespondentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class RespondentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ResponseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(GroupRespondent, GroupRespondentAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Response, ResponseAdmin)
