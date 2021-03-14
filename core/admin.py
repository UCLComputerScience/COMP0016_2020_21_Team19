from django.contrib import admin

from .models import Group, Task, Question


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Question, QuestionAdmin)
