# Generated by Django 3.1.7 on 2021-04-21 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_activity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='blogs',
            new_name='blog',
        ),
    ]
