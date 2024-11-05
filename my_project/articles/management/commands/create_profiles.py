from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Profile

class Command(BaseCommand):
    help = 'Create profile for existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Profiles created for all users.'))
