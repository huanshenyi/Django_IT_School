# Generated by Django 2.0 on 2019-03-07 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20190307_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfavorite',
            old_name='name',
            new_name='user',
        ),
    ]
