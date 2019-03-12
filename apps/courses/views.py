from django.shortcuts import render
from django.views import View
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin


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


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #ユーザーこのコース関連しているのか
        user_coursers = UserCourse.objects.filter(user=request.user, course=course)
        if not user_coursers:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            user_course.save()
        active = 'info'
        status = 'info'
        user_cousers = UserCourse.objects.filter(course=course)

        #このコース受講したほか学生のid
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #すべてのコースidを取得
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #
        relate_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]


        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', context={
         'course': course,
         'active': active,
         'all_resources': all_resources,
         'status': status,
         'relate_course': relate_course
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        active = 'info'
        status = 'comment'
        all_comments = CourseComments.objects.filter(course_id=course_id)
        return render(request, 'course-comment.html', context={
            'course': course,
            'active': active,
            'all_resources': all_resources,
            'status': status,
            'all_comments': all_comments
        })


#レビュー追加
class AddComentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"ログインしてません"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"レビューしました"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"レビュー失敗しました"}', content_type='application/json')


class VideoPlayView(View):
    """
    動画画面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        user_coursers = UserCourse.objects.filter(user=request.user, course=course)
        if not user_coursers:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        active = 'info'
        status = 'info'
        user_cousers = UserCourse.objects.filter(course=course)

        # このコース受講したほか学生のid
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # すべてのコースidを取得
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #
        relate_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', context={
            'course': course,
            'active': active,
            'all_resources': all_resources,
            'status': status,
            'relate_course': relate_course,
            'video': video
        })









