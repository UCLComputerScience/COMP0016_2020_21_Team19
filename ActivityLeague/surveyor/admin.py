from django.contrib import admin
from .models import Group, GroupSurveyor, Question, Surveyor, Task

admin.site.register(Surveyor)
admin.site.register(Task)
admin.site.register(Group)
admin.site.register(GroupSurveyor)
admin.site.register(Question)
