# Generated by Django 3.2.4 on 2021-08-31 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blog_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
