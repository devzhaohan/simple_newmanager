# Generated by Django 2.1.3 on 2018-11-06 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0007_auto_20181106_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_name', models.CharField(max_length=200)),
            ],
        ),
    ]
