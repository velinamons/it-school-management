from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from .enums import AgeGroup, ContactMessageStatus, ManagerRole


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

    def __str__(self):
        return f"{self.name} - {self.course.name}"


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
    phone_number = models.CharField(_("Phone number"), max_length=15, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def __str__(self):
        return self.email


class Student(CustomUser):
    student_groups = models.ManyToManyField(Group, related_name="students", blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Teacher(CustomUser):
    teacher_groups = models.ManyToManyField(Group, related_name="teachers", blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Manager(CustomUser):
    role = models.CharField(
        max_length=20,
        choices=ManagerRole.choices(),
        null=True,
        blank=True,
        help_text="Specify the manager role.",
    )
    managed_filias = models.ManyToManyField(Filia, related_name="managers", blank=True)

    def __str__(self):
        role_display = dict(ManagerRole.choices()).get(self.role, "Manager")
        return f"{self.first_name} {self.last_name} ({role_display})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True, max_length=255)
    suggested_course = models.CharField(max_length=50, null=True)
    suggestion_details = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=20,
        choices=ContactMessageStatus.choices(),
        default=ContactMessageStatus.choices()[0][0],
    )
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
