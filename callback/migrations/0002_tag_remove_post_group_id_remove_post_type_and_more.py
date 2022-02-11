# Generated by Django 4.0.2 on 2022-02-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tags', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='type',
        ),
        migrations.AddField(
            model_name='post',
            name='event_id',
            field=models.CharField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='object',
            field=models.JSONField(),
        ),
    ]
