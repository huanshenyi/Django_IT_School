from django.db import models
from datetime import datetime
from organization.models import CourseOrg


class Course(models.Model):
    # スクールと関連する外部キー
    course_org = models.ForeignKey(CourseOrg, verbose_name="スクール", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"コースネーム")
    desc = models.CharField(max_length=225, verbose_name='コース紹介')
    detail = models.TextField(verbose_name=u'コース詳細')
    """
    easy ->入門
    usual ->中級
    difficult ->上級   
    """
    degree = models.CharField(verbose_name="難易度", choices=(("easy", "入門"), ('usual', '中級'), ('difficult', '上級')), max_length=20)
    learn_time = models.IntegerField(default=0, verbose_name=u'学習時間(分)')
    students = models.IntegerField(default=0, verbose_name=u'学習人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'お気に入り登録人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u'表紙', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'クリック数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u'コース'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"コース", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"セッションネーム")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u"セッション"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"セッション", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"動画ネーム")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u"動画"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"コース", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"資料ネーム")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="資源ファイル", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u"コース資源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
