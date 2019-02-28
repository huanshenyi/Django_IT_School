from django.db import models
from datetime import datetime


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"町")
    desc = models.CharField(max_length=200, verbose_name=u"詳細")
    add_time = models.DateTimeField(verbose_name='追加時間', default=datetime.now)

    class Meta:
        verbose_name = u'町'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"スクール")
    desc = models.TextField(verbose_name=u"スクール説明")
    click_nums = models.IntegerField(default=0, verbose_name=u'クリック数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'気に入り数')
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"ロゴ", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"住所")
    city = models.ForeignKey(CityDict, verbose_name=u"所在地", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='追加時間', default=datetime.now)

    class Meta:
        verbose_name = u'スクール'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属スクール", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="講師ネーム")
    work_years = models.ImageField(default=0, verbose_name="実務年数")
    work_company = models.CharField(max_length=50, verbose_name="所属企業", null=True)
    work_position = models.CharField(max_length=50, verbose_name="役職", null=True)
    points = models.CharField(max_length=50, verbose_name="教育手法", null=True)
    click_nums = models.IntegerField(default=0, verbose_name=u'クリック数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'気に入り数')
    add_time = models.DateTimeField(verbose_name='追加時間', default=datetime.now)

    class Meta:
        verbose_name = u'講師'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


