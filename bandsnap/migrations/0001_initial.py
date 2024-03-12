# Generated by Django 5.0.2 on 2024-03-08 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo', models.ImageField(upload_to='')),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('date', models.DateField()),
                ('venue_address', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('artists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.artist')),
                ('gigs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.gig')),
                ('needs_skills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('accepted', models.BooleanField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.artist')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.band')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='requests',
            field=models.ManyToManyField(through='bandsnap.Request', to='bandsnap.band'),
        ),
        migrations.AddField(
            model_name='artist',
            name='has_skills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bandsnap.skill'),
        ),
    ]