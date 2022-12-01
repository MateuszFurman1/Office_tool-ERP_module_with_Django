# Generated by Django 4.1.3 on 2022-12-01 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office_tool_app', '0005_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_add_medical_leave', 'can add medical leave')],
            },
        ),
    ]