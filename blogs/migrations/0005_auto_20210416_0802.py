# Generated by Django 3.1.7 on 2021-04-16 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_blogs_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='file',
            field=models.TextField(blank=True),
        ),
    ]
