# Generated by Django 3.2.9 on 2021-12-13 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20211211_0131'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobpost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=20)),
                ('job_type', models.CharField(max_length=10)),
                ('job_description', models.TextField()),
                ('job_salary', models.IntegerField()),
                ('job_requirement', models.IntegerField()),
                ('job_tags', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.user')),
            ],
        ),
    ]
