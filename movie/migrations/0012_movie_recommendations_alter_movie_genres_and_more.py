# Generated by Django 5.1.2 on 2025-06-08 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_watchlist_created_at_watchlist_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='recommendations',
            field=models.ManyToManyField(blank=True, to='movie.movie'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movie', to='movie.genre', verbose_name='Жанры'),
        ),
        migrations.AlterField(
            model_name='movieperson',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_person', to='movie.movie'),
        ),
        migrations.AlterField(
            model_name='movieperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_person', to='movie.person', verbose_name='Человек'),
        ),
        migrations.AlterField(
            model_name='movieperson',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='movie_person', to='movie.role', verbose_name='Роли'),
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(default='persons/default.jpg/', upload_to='persons/<django.db.models.fields.CharField>/', verbose_name='Фотографии'),
        ),
    ]
