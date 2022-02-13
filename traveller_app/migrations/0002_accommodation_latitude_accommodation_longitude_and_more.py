# Generated by Django 4.0.1 on 2022-02-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveller_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='latitude',
            field=models.CharField(default=-5.8481119, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accommodation',
            name='longitude',
            field=models.CharField(default=-35.2258358, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='latitude',
            field=models.CharField(default=-35.2258358, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='longitude',
            field=models.CharField(default=-35.2258358, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='latitude',
            field=models.CharField(default=-35.2258358, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='longitude',
            field=models.CharField(default=-35.2258358, max_length=50),
            preserve_default=False,
        ),
    ]