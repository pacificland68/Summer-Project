# Generated by Django 2.2.2 on 2019-08-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_delete_save'),
    ]

    operations = [
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=21)),
                ('listing_id', models.CharField(max_length=20)),
                ('outcode', models.CharField(max_length=20)),
                ('property_type', models.CharField(max_length=20)),
                ('first_published_date_day', models.CharField(max_length=20)),
                ('first_published_date_month', models.CharField(max_length=20)),
                ('first_published_date_year', models.CharField(max_length=20)),
                ('last_published_date_day', models.CharField(max_length=20)),
                ('last_published_date_month', models.CharField(max_length=20)),
                ('last_published_date_year', models.CharField(max_length=20)),
                ('num_bathrooms', models.IntegerField()),
                ('num_bedrooms', models.IntegerField()),
                ('num_floors', models.IntegerField()),
                ('num_recepts', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]
