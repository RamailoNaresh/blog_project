# Generated by Django 5.0.2 on 2024-03-01 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0015_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
