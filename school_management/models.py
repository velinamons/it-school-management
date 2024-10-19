from typing import List

from django.contrib import messages
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from school_management.utils.enums import (
    AgeGroup,
    ManagerRole,
    GroupStatus, EnrollmentStatus, NotificationType,
)
from .utils.decorators.exceptions import exception_handler
from .utils.validators import phone_number_validator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=False)
    last_name = models.CharField(_("Last name"), max_length=150, blank=False)
    phone_number = models.CharField(
        _("Phone number"),
        max_length=15,
        validators=[phone_number_validator],
        blank=False,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        ordering = ["first_name", "last_name"]

    def has_usable_password(self):
        return None

    def __str__(self):
        return self.email


class Student(CustomUser):
    student_groups = models.ManyToManyField(
        "Group", related_name="students", blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(CustomUser):
    teacher_groups = models.ManyToManyField(
        "Group", related_name="teachers", blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Manager(CustomUser):
    role = models.CharField(
        max_length=20,
        choices=ManagerRole.choices(),
        null=True,
        blank=True,
        help_text="Specify the manager role.",
    )

    def __str__(self):
        role_display = dict(ManagerRole.choices()).get(self.role, "Manager")
        return f"{self.first_name} {self.last_name} ({role_display})"


class Filia(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    address = models.CharField(_("Address"), max_length=100)
    description = models.CharField(_("Description"), max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Experience(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    description = models.CharField(_("Description"), max_length=255, blank=True)

    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)

    age_group = models.CharField(
        _("Age Group"), max_length=10, choices=AgeGroup.choices(), blank=True
    )
    experience = models.ManyToManyField(Experience, related_name="courses", blank=True)
    goals = models.ManyToManyField(Goal, related_name="courses", blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    filia = models.ForeignKey(Filia, on_delete=models.CASCADE, related_name="groups")
    status = models.CharField(
        max_length=30,
        choices=GroupStatus.choices(),
        default=GroupStatus.ENROLLMENT_STARTED.value[0],
    )
    group_size = models.IntegerField(
        default=10, validators=[MinValueValidator(2), MaxValueValidator(20)]
    )
    education_start_date = models.DateField(blank=True, null=True)
    education_finish_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.course.name}"

    @transaction.atomic
    @exception_handler
    def add_students(self, student_ids: List[int]) -> bool:
        students = Student.objects.filter(pk__in=student_ids)
        if not students.exists():
            return False
        self.students.add(*students)

        for student in students:
            Notification().create_notification(
                user=student,
                course=self.course,
                operation_type=NotificationType.ADDED.name,
                group=self
            )

        return True

    @transaction.atomic
    @exception_handler
    def add_teachers(self, teacher_ids: List[int]) -> bool:
        teachers = Teacher.objects.filter(pk__in=teacher_ids)
        if not teachers.exists():
            return False
        self.teachers.add(*teachers)

        for teacher in teachers:
            Notification().create_notification(
                user=teacher,
                course=self.course,
                operation_type=NotificationType.ADDED.name,
                group=self
            )

        return True

    @transaction.atomic
    @exception_handler
    def remove_students(self, student_ids: List[int]) -> bool:
        students = self.students.filter(pk__in=student_ids)
        if not students.exists():
            return False
        self.students.remove(*students)

        for student in students:
            Notification().create_notification(
                user=student,
                course=self.course,
                operation_type=NotificationType.REMOVED.name,
                group=self
            )

        return True

    @transaction.atomic
    @exception_handler
    def remove_teachers(self, teacher_ids: List[int]) -> bool:
        teachers = self.teachers.filter(pk__in=teacher_ids)
        if not teachers.exists():
            return False
        self.teachers.remove(*teachers)

        for teacher in teachers:
            Notification().create_notification(
                user=teacher,
                course=self.course,
                operation_type=NotificationType.REMOVED.name,
                group=self
            )

        return True

    @transaction.atomic
    @exception_handler
    def start_education(self, request: HttpRequest) -> bool:
        if not self.students.exists() or not self.teachers.exists():
            messages.error(request, "You cannot start education without students and teachers in the group.")
            return False

        self.status = GroupStatus.EDUCATION_STARTED.value[0]
        self.education_start_date = timezone.now()
        self.save()
        return True

    @transaction.atomic
    @exception_handler
    def finish_education(self, request: HttpRequest) -> bool:
        if not self.status == GroupStatus.EDUCATION_STARTED.value[0]:
            messages.error(request, "You cannot finish education that was not started yet.")
            return False
        self.status = GroupStatus.EDUCATION_COMPLETED.value[0]
        self.education_finish_date = timezone.now()
        self.save()
        return True


class EnrollmentRecord(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices(),
        default=EnrollmentStatus.choices()[0][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enrollment for {self.course} by {self.student}"


class Notification(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.SET_NULL)
    type_of_operation = models.CharField(
        max_length=20,
        choices=NotificationType.choices()
    )
    wide_message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f"Notification: {self.type_of_operation}"

    @transaction.atomic
    @exception_handler
    def create_notification(self, user, course, operation_type, group=None):
        wide_message = ""

        if operation_type == NotificationType.ADDED.name and group:
            wide_message = f"You were added to {course.name} - {group.name}."
        elif operation_type == NotificationType.REJECTED.name:
            wide_message = f"Your enrollment request for {course.name} was rejected."
        elif operation_type == NotificationType.REMOVED.name and group:
            wide_message = f"You were removed from {course.name} - {group.name}."

        notification = Notification(
            user=user,
            course=course,
            group=group,
            type_of_operation=operation_type,
            wide_message=wide_message
        )

        notification.save()
