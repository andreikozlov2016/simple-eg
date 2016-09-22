"""jamanKG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import (
	PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostCreateAPIView,
	)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name = 'list'),
    # url(r'^index/$', index, name = 'index'),
    # url(r'^index0/$', index0),
    # url(r'^base/$', base),
    # url(r'^palette/$', palette),
    # url(r'^popular/$', popular),    
    # url(r'^new_videos/$', new_videos),    
    url(r'^create/$', PostCreateAPIView.as_view(), name = 'create'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name = 'update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name = "delete"),
    
]
