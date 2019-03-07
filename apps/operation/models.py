from django.db import models
from datetime import datetime

from users.models import UserProfile
from courses.models import Course

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="名前")
    mobile = models.CharField(max_length=20, verbose_name="携帯番号")
    course_name = models.CharField(max_length=50, verbose_name="コース名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="挿入時間")

    class Meta:
        verbose_name = "問い合わせ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    """コースレビュー"""
    user = models.ForeignKey(UserProfile, verbose_name=u"ユーザー", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u"コース", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u"レビュー")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="挿入時間")

    class Meta:
        verbose_name = "コースレビュー"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="名前", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="データid")
    fav_type = models.IntegerField(choices=((1, "コース"), (2, "スクール"), (3, "講師")), default=1, verbose_name="お気に入りタイプ")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="挿入時間")

    class Meta:
        verbose_name = "お気に入り"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"メッセージ受けるユーザー")
    message = models.CharField(max_length=500, verbose_name=u"内容")
    has_read = models.BooleanField(default=False, verbose_name="既読か")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="挿入時間")

    class Meta:
        verbose_name = "メッセージ"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"ユーザー", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u"コース", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="挿入時間")

    class Meta:
        verbose_name = "ユーザーコース"
        verbose_name_plural = verbose_name