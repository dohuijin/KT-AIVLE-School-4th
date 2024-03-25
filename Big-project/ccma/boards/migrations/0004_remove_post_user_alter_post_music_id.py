# Generated by Django 4.2.8 on 2024-01-05 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_generatedcontent_username'),
        ('boards', '0003_remove_post_music_file_post_music_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='music_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.generatedcontent'),
        ),
    ]
