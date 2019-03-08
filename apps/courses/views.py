from django.shortcuts import render
from django.views import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite


class CourseListView(View):
    def get(self, request):

        all_course = Course.objects.all().order_by("-add_time")

        #並び替え
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_course = all_course.order_by("-students")
            elif sort == "hot":
                all_course = all_course.order_by('-click_nums')


        #人気コース
        hot_course = all_course.order_by('-click_nums')[:3]

        # スクールリストのページング
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # ここの6は一ページに表示される個数
        p = Paginator(all_course, 9, request=request)
        active = 'course'
        all_course = p.page(page)

        return render(request, 'course-list.html',
                      context={'all_course': all_course,
                               'hot_course': hot_course,
                               'active': active,
                               'sort': sort
                               })

class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        active = 'detail'

        #コースのクリック数を足す
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org =False

        #ユーザー該当コース気に入りしてるかどうか
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

        #ユーザー該当スクールに気に入りしてるかどうか
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag)[:3]
        else:
            relate_coures = []
        return render(request, 'course-detail.html', context={
            'course': course,
            'active': active,
            'relate_coures': relate_coures,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })






