# Generated by Django 2.2.6 on 2019-10-29 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0004_note_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='reminder',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
