from django.urls import path
from . import views


app_name = 'courses'

urlpatterns = [
    #コースリスト
    path("list/", views.CourseListView.as_view(), name='course_list'),
    #コース詳細
    path("detail/<int:course_id>", views.CourseDetailView.as_view(), name='course_detail'),
    #コース内容
    path("info/<int:course_id>", views.CourseInfoView.as_view(), name="course_info"),
    #コースレビュー
    path("comment/<int:course_id>", views.CourseCommentView.as_view(), name="course_comment")

]