# Generated by Django 3.2 on 2022-10-21 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_messages_no_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='post',
            field=models.TextField(),
        ),
    ]
