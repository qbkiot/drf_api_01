# Generated by Django 4.0.1 on 2022-12-06 21:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_petmodel_birthdate_alter_remindermodel_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='petmodel',
            name='birthdate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='remindermodel',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
