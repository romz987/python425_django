from django.core.management import BaseCommand 

import psycopg2
from psycopg2 import sql

from django.conf import settings
#from config.settings import USER, PASSWORD, HOST, DRIVER, PAD_DATABASE, DATABASE 


class Command(BaseCommand):

    def handle(self, *args, **options):
        PAD_DATABASE='postgres'
        USER=settings.DATABASES['default']['USER']
        PASSWORD=settings.DATABASES['default']['PASSWORD']
        HOST=settings.DATABASES['default']['HOST']
        PORT=settings.DATABASES['default']['PORT']
        DATABASE=settings.DATABASES['default']['NAME']
        try:
            conn = psycopg2.connect(
                dbname=PAD_DATABASE,
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT     
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Создаём БД, если не существует
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DATABASE)
                )
            )

        except psycopg2.errors.DuplicateDatabase:
            print(f'База данных {DATABASE} уже существует')
        except Exception as e:
            print(f'Ошибка при создании БД: {e}')
        else:
            print(f'База данных {DATABASE} успешно создана')
        finally:
            if 'conn' in locals():
                conn.close()


