# Generated by Django 4.2.3 on 2023-08-02 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_options_alter_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
