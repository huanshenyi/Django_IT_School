"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url, include
import xadmin
from django.views.generic import TemplateView
from users import views
from organization import views as org_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import reverse



urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url("^$", TemplateView.as_view(template_name="index.html"), name="index"),
    url("login/", views.LoginView.as_view(), name="login"),
    url("register/", views.RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url("active/(?P<active_code>.*)/$", views.ActiveUserView.as_view(), name='user_active'),
    url("forget/", views.ForgetPwdVied.as_view(), name='forget_pwd'),
    url("reset/(?P<active_code>.*)/$", views.ResetView.as_view(), name='reset_pwd'),
    url("modify_pwd/", views.ModifyPwdView.as_view(), name='modify_pwd'),

    #スクールリストホームページ
    url("org_list/", org_views.OrgView.as_view(), name='org_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
