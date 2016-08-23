from django.conf.urls import url
from django.contrib import admin
from testingService import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^testingService/login/$', views.user_login, name='login'),
    url(r'^testingService/logout/$', views.user_logout, name='logout'),
    url(r'^testingService/index/$', views.index, name='index'),
    url(r'^testingService/subject/(?P<subject_id>[0-9]+)/$', views.subject, name='subject'),
    url(r'^testingService/subject/$', views.subject, name='subject'),
]
