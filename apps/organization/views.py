from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict


class OrgView(View):
    def get(self, request):
        #すべてのスクール
        all_orgs = CourseOrg.objects.all()
        #すべての都市
        all_citys = CityDict.objects.all()

        return render(request, 'org-list.html', context={
           'all_orgs': all_orgs, 'all_citys': all_citys
        })
