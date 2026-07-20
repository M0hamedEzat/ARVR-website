from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_annotation_status_annotation_audio_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='annotation-images/'),
        ),
    ]