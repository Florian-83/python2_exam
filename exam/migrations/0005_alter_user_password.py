# Generated by Django 5.0.1 on 2024-02-10 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
