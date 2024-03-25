# Generated by Django 4.2.7 on 2024-01-10 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_generatedcontent_image_name"),
        ("video", "0003_editedvideo_video_name_alter_editedvideo_video_file"),
        ("boards", "0005_post_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="video_id",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="video.editedvideo",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="music_id",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.generatedcontent",
            ),
        ),
    ]
