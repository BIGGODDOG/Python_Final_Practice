from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from articles.models import Article
from users.models import UserProfile  # Модель пользователя, если она кастомная

class Command(BaseCommand):
    help = 'Создает группу "Administrators" с необходимыми правами'

    def handle(self, *args, **kwargs):
        # Создаем группу администраторов
        admin_group, created = Group.objects.get_or_create(name='Administrators')

        # Назначаем права на управление статьями
        article_content_type = ContentType.objects.get_for_model(Article)
        article_permissions = Permission.objects.filter(content_type=article_content_type)
        admin_group.permissions.add(*article_permissions)

        # Назначаем права на управление пользователями
        user_content_type = ContentType.objects.get_for_model(UserProfile)
        user_permissions = Permission.objects.filter(content_type=user_content_type)
        admin_group.permissions.add(*user_permissions)

        self.stdout.write(self.style.SUCCESS('Группа "Administrators" успешно создана и права назначены'))
