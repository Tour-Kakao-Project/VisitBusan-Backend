# Generated by Django 4.2.3 on 2023-09-25 14:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0008_member_is_authorized"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="phone_number",
        ),
    ]