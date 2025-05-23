# Generated by Django 5.1.7 on 2025-05-23 08:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_cast_options_alter_klient_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OblibenaNemovitost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vytvoreno', models.DateTimeField(auto_now_add=True)),
                ('nemovitost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lajky', to='main.nemovitost')),
                ('uzivatel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('uzivatel', 'nemovitost')},
            },
        ),
    ]
