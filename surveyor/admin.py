from django.contrib import admin

from .models import GroupSurveyor, Surveyor, Organisation, TaskTemplate, QuestionTemplate


class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class SurveyorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class GroupSurveyorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class TaskTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class QuestionTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Surveyor, SurveyorAdmin)
admin.site.register(GroupSurveyor, GroupSurveyorAdmin)
admin.site.register(TaskTemplate, TaskTemplateAdmin)
admin.site.register(QuestionTemplate, QuestionTemplateAdmin)
