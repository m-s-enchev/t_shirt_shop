# Generated by Django 4.2.3 on 2023-08-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='address',
            field=models.TextField(max_length=100),
        ),
    ]
