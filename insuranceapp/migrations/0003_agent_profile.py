# Generated by Django 5.0.6 on 2024-06-03 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insuranceapp', '0002_agent_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='profile',
            field=models.ImageField(null=True, upload_to='image/'),
        ),
    ]