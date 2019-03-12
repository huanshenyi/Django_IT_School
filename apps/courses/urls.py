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
    #コースレビュー画面
    path("comment/<int:course_id>", views.CourseCommentView.as_view(), name="course_comment"),
    #レビュー
    path("add_comment/", views.AddComentsView.as_view(), name="add_comment"),
    #動画画面
    path("video/<int:video_id>", views.VideoPlayView.as_view(), name="video_play")

]