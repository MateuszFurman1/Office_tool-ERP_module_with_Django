# Generated by Django 4.1.3 on 2022-11-29 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office_tool_app', '0003_messages_sending_date_alter_delegation_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='messages',
            unique_together=set(),
        ),
    ]
