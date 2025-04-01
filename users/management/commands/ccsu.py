from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options): 
        admin_user = User.objects.create(
            email = 'admin@my_host.su',
            first_name = 'admin',
            last_name= 'admin',
            is_staff= True,
            is_superuser=True,
            is_active=True
        )

        admin_user.set_password('qwerty')
        admin_user.save()
        print('Admin Created')
