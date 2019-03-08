from django.shortcuts import render
from django.views import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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






