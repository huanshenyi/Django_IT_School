# Generated by Django 2.0 on 2019-03-04 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190228_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverifyrecord',
            options={'verbose_name': 'メール検証コード', 'verbose_name_plural': 'メール検証コード'},
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='発行時間'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '新規ユーザー'), ('forget', 'パスワード再発行')], max_length=15, verbose_name='コードタイプ'),
        ),
    ]
