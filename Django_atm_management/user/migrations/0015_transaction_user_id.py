# Generated by Django 5.0.7 on 2024-07-29 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_user_deposit_amount_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
