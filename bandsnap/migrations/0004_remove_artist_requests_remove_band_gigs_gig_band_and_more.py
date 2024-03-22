# Generated by Django 5.0.2 on 2024-03-20 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandsnap', '0003_alter_artist_photo_alter_band_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='requests',
        ),
        migrations.RemoveField(
            model_name='band',
            name='gigs',
        ),
        migrations.AddField(
            model_name='gig',
            name='band',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='gigs', to='bandsnap.band'),
        ),
        migrations.AddField(
            model_name='request',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.RemoveField(
            model_name='band',
            name='artists',
        ),
        migrations.RemoveField(
            model_name='band',
            name='needs_skills',
        ),
        migrations.AlterField(
            model_name='request',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('artist', 'band')},
        ),
        migrations.AddField(
            model_name='band',
            name='artists',
            field=models.ManyToManyField(through='bandsnap.Request', to='bandsnap.artist'),
        ),
        migrations.AddField(
            model_name='band',
            name='needs_skills',
            field=models.ManyToManyField(to='bandsnap.skill'),
        ),
    ]