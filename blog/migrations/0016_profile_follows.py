# Generated by Django 3.2.4 on 2021-09-03 01:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_remove_profile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(related_name='profile_page', to=settings.AUTH_USER_MODEL),
        ),
    ]
