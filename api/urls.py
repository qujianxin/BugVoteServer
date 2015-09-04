from BugVote import settings
from api import views, urls_restful

__author__ = 'hason'

from django.conf.urls import url, include

urlpatterns = [
    url(r"m/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
    url(r'^$', views.index_view),
    url(r"^api/", include(urls_restful)),
    url(r"^register/$", views.register_view),
    url(r"^login/$", views.login_view),
    url(r"^submit/$", views.submit_view),
    url(r"^person/$", views.person_view),
    url(r"^news/(?P<pk>\d+)/$", views.news_view),
    url(r"^rank_list/$", views.rank_list_view),
    url(r"^news_list/$", views.news_list_view),
    # 后台界面
    url(r"^manage/$", views.manage_view),
    url(r"^manage/user_list/$", views.manage_user_list),
    url(r"^manage/rank_list/$", views.manage_rank_list),
    url(r"^manage/bug_list/$", views.manage_bug_list),
    url(r"^manage/news_list/$", views.manage_news_list),
    url(r"^manage/system_setting/$", views.manage_system_setting),
    url(r"^manage/post_news/$", views.manage_post_news),
    url(r"^manage/check_news/$", views.manage_check_news),

]
