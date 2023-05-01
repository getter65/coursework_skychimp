from django.contrib import admin

from school.models import Lesson, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description', 'slug', 'course')
    prepopulated_fields = {"slug": ("name", "description")}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description')
    # prepopulated_fields = {"pk": ("name", "description")}
