from django.contrib.auth.forms import UserCreationForm
from .models import User


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
