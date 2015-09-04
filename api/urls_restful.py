from api import views_restful

__author__ = 'hason'

from django.conf.urls import url

urlpatterns = [url("^check_phone/$", views_restful.check_phone),
               url("^validate_phone/$", views_restful.validate_phone),
               url("^register/$", views_restful.register),
               url("^log_in/$", views_restful.login_user),
               url("^log_out/$", views_restful.logout_user),
               url("^submit_bug/$", views_restful.post_one_record),
               url("^edit_user/$", views_restful.edit_user),
               url("^send_msg/$", views_restful.send_msg),
               # 后台管理
               url("^manage/login/$", views_restful.manage_login),
               url("^manage/logout/$", views_restful.manage_logout),
               url("^manage/post_news/$", views_restful.post_news),
               url("^manage/delete_news/$", views_restful.delete_news),
               url("^manage/update_news/$", views_restful.update_news),
               url("^manage/delete_publicity/$", views_restful.delete_publicity),
               url("^manage/post_publicity/$", views_restful.post_publicity),
               url("^manage/update_end_time/$", views_restful.update_end_time),
               url("^manage/update_bonus/$", views_restful.update_bonus),
               url("^manage/update_bug_type/$", views_restful.update_bug_type),
               url("^manage/post_bug_type/$", views_restful.add_bug_type),
               ]
