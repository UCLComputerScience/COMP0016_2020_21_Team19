from django.contrib import admin
from .models import Group, GroupSurveyor, Question, Surveyor, Task

class SurveyorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class GroupSurveyorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Surveyor, SurveyorAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupSurveyor, GroupSurveyorAdmin)
admin.site.register(Question, QuestionAdmin)
