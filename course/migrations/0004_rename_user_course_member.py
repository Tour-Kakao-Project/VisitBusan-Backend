# Generated by Django 4.2.3 on 2023-09-09 06:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0003_course_total_people_cnt_course_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="user",
            new_name="member",
        ),
    ]