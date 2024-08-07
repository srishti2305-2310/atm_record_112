# Generated by Django 5.0.7 on 2024-07-22 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_create_user_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default="2024-07-16 15:41:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username', 'password'], name='user_user_usernam_ea9a53_idx'),
        ),
    ]
