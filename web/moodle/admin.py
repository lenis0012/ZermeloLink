from django.contrib import admin

# Register your models here.
from .models import Subject, Cohort

class CohortInline(admin.TabularInline):
    model = Cohort
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    inlines = [CohortInline]

admin.site.register(Subject, SubjectAdmin)