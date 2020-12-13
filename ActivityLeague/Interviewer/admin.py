from django.contrib import admin
from .models import *

admin.site.register(Interviewer)
admin.site.register(Task)
admin.site.register(Group)
admin.site.register(GroupInterviewer)