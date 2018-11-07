from django.conf.urls import url
from Api import views

urlpatterns = [
    url(r'^add_news/$', views.add_news_job),
    url(r'^remove_news/$', views.remove_news_job),
    url(r'^modify_news/$', views.modify_news_job),
    url(r'^login/$', views.login_job),
    url(r'^create_member/$', views.create_member_job),
    url(r'^modify_member/$', views.modify_member_job),
    url(r'^list_member/$', views.list_member_job),


    url(r'^list_news/$', views.list_news_job),
    url(r'^show_news/$', views.show_news_job),


]