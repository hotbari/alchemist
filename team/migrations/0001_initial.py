# Generated by Django 5.0.6 on 2025-03-26 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('club', '__first__'),
        ('image_url', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='club.club')),
                ('image_url', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='image_url.imageurl')),
            ],
            options={
                'db_table': 'team',
            },
        ),
    ]
