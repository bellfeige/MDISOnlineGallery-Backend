# Generated by Django 2.2.13 on 2020-07-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
