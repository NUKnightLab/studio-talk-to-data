# Generated by Django 2.0.2 on 2018-02-23 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_flow', '0002_auto_20180223_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='deleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='deleted',
            field=models.DateTimeField(null=True),
        ),
    ]
