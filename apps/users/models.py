from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserProfile(AbstractUser):
    """AbstractUserを継承してdefaultのuserテーブルを取って代わる"""
    nick_name = models.CharField(max_length=50, verbose_name=u'ニックネーム', default='')
    birday = models.DateField(verbose_name=u"誕生日", null=True)
    gender = models.CharField(max_length=10, choices=(('male', u"男性"), ('female', u'女性'),
                                       ('otherwise', u'その他')), default="male")
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "ユーザーデータ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"検証コード")
    email = models.EmailField(max_length=50, verbose_name=u"メールアドレス")
    send_type = models.CharField(verbose_name="コードタイプ", choices=(("register", u"新規ユーザー"),
                                          ('forget', u'パスワード再発行')), max_length=15)
    send_time = models.DateTimeField(verbose_name="発行時間", default=datetime.now)

    class Meta:
        verbose_name = u"メール検証コード"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


"""スライド"""
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"タイトル")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name='スライド', max_length=100)
    url = models.URLField(max_length=200, verbose_name=u'url')
    index = models.IntegerField(default=100, verbose_name=u'順番')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u"スライド"
        verbose_name_plural = verbose_name