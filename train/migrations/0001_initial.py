# Generated by Django 5.0.4 on 2024-04-18 17:09

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=255)),
                ('train_capacity', models.IntegerField()),
                ('source', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('occupancy', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seat_number', models.IntegerField()),
                ('is_booked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.train')),
            ],
        ),
    ]
