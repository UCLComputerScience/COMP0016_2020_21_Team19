from django.contrib import admin
from .models import *

class Admin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Interviewer, Admin)
admin.site.register(Task, Admin)
admin.site.register(Group, Admin)
admin.site.register(GroupInterviewer, Admin)
admin.site.register(Question, Admin)