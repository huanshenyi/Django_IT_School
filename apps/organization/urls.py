from django.conf.urls import url
from .views import OrgView,AddUserAskView

app_name = 'organization'


urlpatterns = [

    #スクールリスト
    url("list/", OrgView.as_view(), name='org_list'),
    url("add_ask/", AddUserAskView.as_view(), name='add_ask')

]