# Generated by Django 2.2.13 on 2020-07-12 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digitalartpreviewimg',
            name='digital_art',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previewImgs', to='api.DigitalArt'),
        ),
        migrations.AlterField(
            model_name='digitalartpreviewimg',
            name='image_sequence',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
