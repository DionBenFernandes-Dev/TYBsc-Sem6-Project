# Generated by Django 3.0 on 2021-05-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_member_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
