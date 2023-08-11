# Generated by Django 4.2.3 on 2023-08-10 19:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_userprofilemodel_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
