# Generated by Django 3.2.7 on 2021-09-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='css_class',
        ),
        migrations.AlterField(
            model_name='plan',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]