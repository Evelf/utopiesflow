from django.conf.urls import url

from pinapp import views


urlpatterns = [
    url(r'^$', views.BoardList.as_view(), name='index'),
    url(r'^board/(?P<pk>[0-9]+)$', views.BoardDetail.as_view(), name='board'),
]
