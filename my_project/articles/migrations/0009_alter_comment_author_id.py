# Generated by Django 5.1.1 on 2024-11-05 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_rename_address_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.profile'),
        ),
    ]
