from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User, Student, Worker


@receiver(post_save, sender=User)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Worker)
def gen_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
