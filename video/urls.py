from django.conf.urls import include, url
from video import views

 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^video_request',views.video_request),
]
