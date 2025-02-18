# Generated by Django 5.0.4 on 2024-04-30 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmotionEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('emotion_level', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('emotion_type', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('activity', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
