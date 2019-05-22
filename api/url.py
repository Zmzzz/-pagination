from django.conf.urls import url,include
from django.contrib import admin
from  api import  views
urlpatterns = [
    url(r'^course/$',views.course.as_view({'get':'list'})),
    url(r'^course/(?P<pk>\d+)/$', views.course.as_view({'get':'retrieve'})),
    url(r'^login/',views.login.as_view()),
    url(r'^mrio/',views.mrio.as_view())
]