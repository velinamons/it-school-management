from django.contrib import admin
from .models import (
    Filia,
    Course,
    Group,
    Student,
    Teacher,
    Manager,
    Experience,
    Goal

)


@admin.register(Filia)
class FiliaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    search_fields = ('name', 'city')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('experience', 'goals')
    search_fields = ('name', 'age_group', 'experience', 'goals')

    def experience_list(self, obj):
        return ", ".join([exp.name for exp in obj.experience.all()])
    experience_list.short_description = 'Experience'

    def goals_list(self, obj):
        return ", ".join([goal.name for goal in obj.goals.all()])
    goals_list.short_description = 'Goals'

    list_display = ('name', 'age_group', 'experience_list', 'goals_list')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'filia')
    list_filter = ('course', 'filia')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'password',
        'first_name',
        'last_name',
        'phone_number',
        'is_active',
        'student_groups'
    )

    exclude = ('is_staff', 'last_login', 'is_superuser', 'groups', 'user_permissions')
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'password',
        'first_name',
        'last_name',
        'phone_number',
        'is_active',
        'teacher_groups'
    )
    exclude = ('is_staff', 'last_login', 'is_superuser', 'groups', 'user_permissions')
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'managed_filia_list')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'managed_filias__name')
    filter_horizontal = ('managed_filias',)
    fields = (
        'email',
        'password',
        'first_name',
        'last_name',
        'phone_number',
        'role',
        'is_active',
        'managed_filias',
    )
    exclude = ('is_staff', 'last_login', 'is_superuser', 'groups', 'user_permissions')

    def managed_filia_list(self, obj):
        return ", ".join([filia.name for filia in obj.managed_filias.all()])

    managed_filia_list.short_description = 'Managed Filias'