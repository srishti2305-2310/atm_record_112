# Generated by Django 5.0.7 on 2024-07-29 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deposit_amount',
            field=models.FloatField(default=0),
        ),
    ]