# Generated by Django 4.2 on 2023-04-28 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_community_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
