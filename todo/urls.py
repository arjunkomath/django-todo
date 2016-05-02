from django.conf.urls import url, include
from django.contrib import admin

from todoapp import views, api

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^api/todo/$', api.todo),
	url(r'^api/todo/(?P<id>\w+)$', api.todo),
	url(r'^admin/', admin.site.urls),
]
