from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from django.http import HttpResponse


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
