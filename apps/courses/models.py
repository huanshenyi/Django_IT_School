from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    # スクールと関連する外部キー
    course_org = models.ForeignKey(CourseOrg, verbose_name="スクール", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"コースネーム")
    desc = models.CharField(max_length=225, verbose_name='コース紹介')
    detail = models.TextField(verbose_name=u'コース詳細')
    teacher = models.ForeignKey(Teacher, verbose_name="講師", null=True, blank=True, on_delete=models.CASCADE)
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
    category = models.CharField(verbose_name='コース区分', max_length=20, default='ウェブ開発')
    tag = models.CharField(default='', verbose_name='コースラベル', max_length=10)
    youneed_know = models.CharField(max_length=300, verbose_name='学習前提', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name='講師からのメッセージ', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u'コース'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #セッション数を取得
        return self.lesson_set.all().count()

    #このコース学習してるユーザー
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #コースのセッションを取得
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"コース", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"セッションネーム")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"挿入時間")

    class Meta:
        verbose_name = u"セッション"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        #セッションの動画を取得
        return self.video_set.all()

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"セッション", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"動画ネーム")
    url = models.CharField(max_length=200, verbose_name='動画url', default="")
    learn_time = models.IntegerField(default=0, verbose_name=u'学習時間(分)')
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
