# Generated by Django 2.2 on 2021-04-17 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fav_books_app', '0003_auto_20210417_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='liked_by',
            field=models.ManyToManyField(related_name='books_liked', to='fav_books_app.User'),
        ),
        migrations.AlterField(
            model_name='book',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_added', to='fav_books_app.User'),
        ),
    ]
