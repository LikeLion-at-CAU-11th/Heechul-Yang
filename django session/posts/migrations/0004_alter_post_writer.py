# Generated by Django 4.1.7 on 2023-07-07 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.CharField(max_length=30, verbose_name='작성자'),
        ),
    ]