# Generated by Django 3.2 on 2022-10-21 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_messages_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='post_category',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='messages',
            name='post_thumbnail',
            field=models.TextField(),
        ),
    ]
