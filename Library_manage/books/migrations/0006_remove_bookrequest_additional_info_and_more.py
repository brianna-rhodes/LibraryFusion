# Generated by Django 5.0.2 on 2025-05-05 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_bookrequest_delete_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrequest',
            name='additional_info',
        ),
        migrations.AddField(
            model_name='bookrequest',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted')], default='PENDING', max_length=10),
        ),
    ]
