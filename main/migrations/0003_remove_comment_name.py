# Generated by Django 2.1.7 on 2020-05-01 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]