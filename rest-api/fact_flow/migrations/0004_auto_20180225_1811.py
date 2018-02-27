# Generated by Django 2.0.1 on 2018-02-26 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_flow', '0003_auto_20180223_0158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claim',
            options={'ordering': ('article_id',)},
        ),
        migrations.AddField(
            model_name='claim',
            name='source_id',
            field=models.UUIDField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='article_id',
            field=models.UUIDField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='verified',
            field=models.DateTimeField(null=True),
        ),
    ]
