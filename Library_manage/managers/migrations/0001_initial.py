# Generated by Django 5.2 on 2025-04-27 23:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, help_text='The amount of the fine', max_digits=10)),
                ('reason', models.TextField(help_text='The reason for issuing this fine')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When this fine was created')),
                ('paid', models.BooleanField(default=False, help_text='Whether this fine has been paid')),
                ('paid_at', models.DateTimeField(blank=True, help_text='When this fine was paid', null=True)),
                ('borrowing_record', models.ForeignKey(help_text='The borrowing record this fine is associated with', on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='books.borrowingrecord')),
                ('created_by', models.ForeignKey(help_text='The user who created this fine', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_fines', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fine',
                'verbose_name_plural': 'Fines',
                'ordering': ['-created_at'],
            },
        ),
    ]
