# Generated by Django 2.0 on 2019-03-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20190306_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='work_years',
            field=models.IntegerField(default=0, verbose_name='実務年数'),
        ),
    ]
