from .models import *
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.shortcuts import reverse
from django.utils.html import format_html


# Register your models here.

class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 2
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'survey'
    inlines = [AnswerInline]


class SurveyAdmin(NestedModelAdmin):
    list_display = ('topic', 'description', 'view_results')
    model = Survey
    inlines = [QuestionInline]
    search_fields = ['topic', 'description']
    current_url = ""

    def view_results(self, obj):
        return format_html(
            "<a href='{url}'>View</a>",
            url=reverse("surveys:results", kwargs={"pk": obj.id})
        )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        self.current_url = request.get_full_path()
        print(self.current_url)
        qs = super(SurveyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user)


class QuestionAdmin(admin.ModelAdmin):
    model = Question

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                'add': self.has_add_permission(request),
                'change': self.has_change_permission(request),
                'delete': self.has_delete_permission(request),
                'view': self.has_view_permission(request),
            }
        else:
            return {}


class AnswerAdmin(admin.ModelAdmin):
    model = Answer

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                'add': self.has_add_permission(request),
                'change': self.has_change_permission(request),
                'delete': self.has_delete_permission(request),
                'view': self.has_view_permission(request),
            }
        else:
            return {}


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Rating)
