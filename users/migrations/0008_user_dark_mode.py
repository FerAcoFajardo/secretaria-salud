# Generated by Django 4.0.2 on 2022-03-07 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
    ]
