from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from operation.models import UserFavorite
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    def get(self, request):
        #すべてのスクール
        all_orgs = CourseOrg.objects.all()
        #すべての都市
        all_citys = CityDict.objects.all()

        #スクールランキング(クリック数)
        hot_orgs = all_orgs.order_by("-click_nums")[:5]

        #cityの検索
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #カテゴリの検索
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        #学習人数の並び替え
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
               all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by('-course_nums')


        #スクールリストのページング
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #ここの6は一ページに表示される個数
        p = Paginator(all_orgs, 6, request=request)

        orgs = p.page(page)
        org_num = all_orgs.count()
        return render(request, 'org-list.html', context={
           'all_orgs': orgs,
           'all_citys': all_citys,
            'city_id': city_id,
            'category': category,
            'org_num': org_num,
            'hot_orgs': hot_orgs,
            'sort': sort
        })

class AddUserAskView(View):
    """
    問い合わせ
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"送信失敗"}', content_type='application/json')


#スクールホームページ
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                                    fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html',
                      context={'all_courses': all_courses,
                               'all_teachers': all_teachers,
                               'course_org': course_org,
                               'current_page': current_page,
                               'has_fav': has_fav
                               })


#スクールコースリスト
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'coures'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()


        return render(request, 'org-detail-course.html',
                      context={'all_courses': all_courses,
                               'course_org': course_org,
                               'current_page': current_page,
                               'has_fav': has_fav
                               })


#スクール詳細
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True

        return render(request, 'org-detail-desc.html',
                      context={
                               'course_org': course_org,
                               'current_page': current_page,
                               'has_fav': has_fav
                               })


#スクール講師
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        return render(request, 'org-detail-teachers.html',
                      context={
                               'course_org': course_org,
                               'current_page': current_page,
                               'all_teachers': all_teachers,
                               'has_fav': has_fav
                               })


class AddFavView(View):
    """
    お気に入り登録，お気に入りの削除
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # ログインしてかどうかを判断
        if not request.user.is_authenticated:
           return HttpResponse('{"status":"fail","msg":"登録してない"}',
                               content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,
                                                    fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #もし記録存在していれば,お気に入りを削除
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"お気に入り登録"}',
                                content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"お気入"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"登録失敗"}',
                                    content_type='application/json')
