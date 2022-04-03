from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserCreationForm
from .models import User, Complaint


class NewUserAdmin(UserAdmin):
    model = User
    add_form = NewUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Additional data",
            {"fields": ("name", "contact_number", "hostel", "room_number", "usertype")},
        ),
    )


admin.site.register(User, NewUserAdmin)
admin.site.register(Complaint)
