# Generated by Django 4.1.3 on 2022-12-01 20:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
