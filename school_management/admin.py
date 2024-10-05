from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Filia, Course, Group, Student, Teacher, Manager, Experience, Goal


class BaseUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("last_name",)
    exclude = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions", {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    class Media:
        js = ("js/scripts.js",)


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Student Details", {"fields": ("student_groups",)}),
    )
    list_display = BaseUserAdmin.list_display + ("student_groups_list",)
    filter_horizontal = ("student_groups",)

    @admin.display(description="Student Groups")
    def student_groups_list(self, obj):
        return ", ".join([filia.name for filia in obj.student_groups.all()])


@admin.register(Teacher)
class TeacherAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Teacher Details", {"fields": ("teacher_groups",)}),
    )
    list_display = BaseUserAdmin.list_display + ("teacher_groups_list",)
    filter_horizontal = ("teacher_groups",)

    @admin.display(description="Teacher Groups")
    def teacher_groups_list(self, obj):
        return ", ".join([filia.name for filia in obj.teacher_groups.all()])


@admin.register(Manager)
class ManagerAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Manager Details", {"fields": ("role", "managed_filias")}),
    )
    list_display = BaseUserAdmin.list_display + ("role", "managed_filia_list")
    filter_horizontal = ("managed_filias",)

    @admin.display(description="Managed Filias")
    def managed_filia_list(self, obj):
        return ", ".join([filia.name for filia in obj.managed_filias.all()])


@admin.register(Filia)
class FiliaAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address")
    search_fields = ("name", "city")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ("experience", "goals")
    search_fields = ("name", "age_group", "experience", "goals")

    @admin.display(description="Experience")
    def experience_list(self, obj):
        return ", ".join([exp.name for exp in obj.experience.all()])

    @admin.display(description="Goals")
    def goals_list(self, obj):
        return ", ".join([goal.name for goal in obj.goals.all()])

    list_display = ("name", "age_group", "experience_list", "goals_list")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "filia")
    list_filter = ("course", "filia")
    search_fields = ("name",)
