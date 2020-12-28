# Generated by Django 3.1.4 on 2020-12-28 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('summary', models.CharField(max_length=300)),
                ('link', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
    ]