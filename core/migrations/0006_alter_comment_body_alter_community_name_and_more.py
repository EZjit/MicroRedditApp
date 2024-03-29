# Generated by Django 4.2 on 2023-04-27 13:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_community_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.community', verbose_name='Choose a community'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
