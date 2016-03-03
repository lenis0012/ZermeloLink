from django.contrib import admin

from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInLine]

# Register your models here.
admin.site.register(Question, QuestionAdmin)
