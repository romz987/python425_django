from django.core.management.base import BaseCommand
from users.models import User, UserRoles


class Command(BaseCommand):

    def handle(self, *args, **options): 
        admin = User.objects.create(
            email='admin@myhost.su',
            first_name='Admin',
            last_name='Adminov',
            role=UserRoles.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        admin.set_password('qwerty')
        admin.save()
        print('Admin Created')


        moderator = User.objects.create(
            email='moderator@myhost.su',
            first_name='Moder',
            last_name='Moderov',
            role=UserRoles.MODERATOR,
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        moderator.set_password('qwerty')
        moderator.save()
        print('Moderator Created')


        user = User.objects.create(
            email='user1@myhost.su',
            first_name='User',
            last_name='Userov',
            role=UserRoles.USER,
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password('qwerty')
        user.save()
        print('User Created')
