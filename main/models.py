from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_("name"), max_length=300, blank=True)
    contact_number = models.CharField(_("contact number"), max_length=16, blank=True)
    roll_number = models.CharField(_("roll number"), max_length=20, blank=True)
    room_number = models.CharField(_("room number"), max_length=10, blank=True)

    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        ELECTRICIAN = "ELECTRICIAN", "Electrician"
        CARPENTER = "CARPENTER", "Carpenter"
        CLEANER = "CLEANER", "Cleaner"
        PLUMBER = "PLUMBER", "Plumber"
        OTHERS = "OTHERS", "Others"

    default_type = Types.STUDENT
    usertype = models.CharField(
        _("user type"), max_length=12, choices=Types.choices, default=Types.STUDENT
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.usertype = self.default_type
        return super().save(*args, **kwargs)


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(usertype=User.Types.STUDENT)


class WorkerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(usertype=any(User.Types.choices[1:]))
        )


class Student(User):
    default_type = User.Types.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True


class Worker(User):
    default_type = User.Types.OTHERS
    objects = WorkerManager()

    class Meta:
        proxy = True


class Complaint(models.Model):
    class ComplaintTypes(models.TextChoices):
        ELECTRICIAN = "ELECTRICIAN", "Electrician"
        CARPENTER = "CARPENTER", "Carpenter"
        CLEANER = "CLEANER", "Cleaner"
        PLUMBER = "PLUMBER", "Plumber"
        OTHERS = "OTHERS", "Others"

    type = models.CharField(_("type"), max_length=100, choices=ComplaintTypes.choices)
    description = models.TextField(_("description"))
    date_lodged = models.DateTimeField(_("date logged"), auto_now_add=True)
    mark_done = models.BooleanField(_("done by student"), default=False)
    roll_number = models.CharField(
        _("roll number"), max_length=20, blank=True, default=""
    )
    room_number = models.CharField(
        _("room number"), max_length=10, blank=True, default=""
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        related_name="student",
        null=True,
        blank=True,
    )
    contact_number = models.CharField(_("contact number"), max_length=16, blank=True)

    class Meta:
        ordering = ["-date_lodged"]

    def __str__(self) -> str:
        return f"#{self.id} {self.type}"
