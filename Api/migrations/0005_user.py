# Generated by Django 2.1.3 on 2018-11-06 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_auto_20181106_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='用户名')),
                ('passwd', models.CharField(max_length=50, verbose_name='密码')),
                ('active', models.CharField(max_length=2, verbose_name='是否激活')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
            ],
        ),
    ]
