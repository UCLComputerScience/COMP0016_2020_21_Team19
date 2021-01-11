from django.contrib import admin
from .models import Respondent, Response, GroupRespondent

admin.site.register(GroupRespondent)
admin.site.register(Respondent)
admin.site.register(Response)
