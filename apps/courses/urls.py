from django.urls import path
from . import views


app_name = 'courses'

urlpatterns = [
    #コースリスト
    path("list/", views.CourseListView.as_view(), name='course_list'),

]