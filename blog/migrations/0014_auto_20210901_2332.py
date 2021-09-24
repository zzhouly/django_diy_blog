# Generated by Django 3.2.4 on 2021-09-02 06:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0013_auto_20210901_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='followers',
        ),
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(related_name='blog_follow', to=settings.AUTH_USER_MODEL),
        ),
    ]