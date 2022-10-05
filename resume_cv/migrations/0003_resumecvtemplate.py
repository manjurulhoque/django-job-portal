# Generated by Django 4.0.1 on 2022-03-28 14:46

import django.db.models.deletion
from django.db import migrations
from django.db import models

import resume_cv.models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_cv', '0002_resumecvcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeCvTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=resume_cv.models.resume_cv_directory_path)),
                ('content', models.TextField(blank=True, null=True)),
                ('style', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='resume_cv.resumecvcategory')),
            ],
        ),
    ]
