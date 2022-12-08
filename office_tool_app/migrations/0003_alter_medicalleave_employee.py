# Generated by Django 4.1.3 on 2022-12-08 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office_tool_app', '0002_alter_addresscore_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalleave',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_employee', to=settings.AUTH_USER_MODEL),
        ),
    ]