# Generated by Django 2.2.13 on 2020-07-12 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200712_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='price',
            new_name='price_in_all',
        ),
        migrations.RemoveField(
            model_name='order',
            name='digital_art',
        ),
        migrations.RemoveField(
            model_name='order',
            name='download_url',
        ),
        migrations.RemoveField(
            model_name='order',
            name='title',
        ),
        migrations.CreateModel(
            name='OrderDigitalArt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('download_url', models.URLField()),
                ('price', models.FloatField()),
                ('digital_art', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_digital_art', to='api.DigitalArt')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_digital_art', to='api.Order')),
            ],
        ),
    ]
