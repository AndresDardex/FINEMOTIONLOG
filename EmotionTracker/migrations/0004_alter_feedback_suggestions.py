# Generated by Django 5.0.6 on 2024-06-05 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmotionTracker', '0003_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='suggestions',
            field=models.TextField(default=''),
        ),
    ]
