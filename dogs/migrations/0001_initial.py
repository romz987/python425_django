# Generated by Django 5.2 on 2025-04-02 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='breed')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
            ],
            options={
                'verbose_name': 'breed',
                'verbose_name_plural': 'breeds',
            },
        ),
    ]
