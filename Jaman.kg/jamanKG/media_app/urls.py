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
from django.conf.urls import *
from django.contrib import admin


from media_app.views import (
    DashboardTemplateView, 
    MyView, 
    TagView,
    PostDetail,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
  )


#from media_app.views import (
    # TagIndexView,
    # IndexView,
    # PostDetailView,
	# post_list,
	# post_create,
	# post_detail,
	# post_update,
	# post_delete,
    #    popular,
    #    palette,
    #    #index,
    #    base,
    #    index0,
    #    new_videos,
    #video_test,

	#)

urlpatterns = [
    url(r'^categories/(?P<slug>[-\w]+)/$', TagView.as_view(), name='tagged'),
    url(r'^create/$', PostCreateView.as_view(), name = 'create'),    
    url(r'^about/$', DashboardTemplateView.as_view(), name = 'about'),
    url(r'^someview/$', MyView.as_view(template_name = "index.html"), name = 'someview'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetail.as_view(), name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateView.as_view(), name = 'update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteView.as_view(), name = 'delete'),
    url(r'^$', PostListView.as_view(), name = 'index'),
    
    # #url(r'^$', index, name = 'index'),
    # url(r'^$', IndexView.as_view(), name = 'index'),
    #url(r'^video/$', video_test, name = 'video'),
    # url(r'^post_list/$', post_list, name = 'post_list'),
    # url(r'^index0/$', index0),
    # url(r'^base/$', base),
    # url(r'^palette/$', palette),
    # url(r'^popular/$', popular),    
    # url(r'^new_videos/$', new_videos),    
    # url(r'^create/$', post_create, name = 'create'),
    # #url(r'^(?P<slug>[\w-]+)/$', post_detail, name = 'detail'),
    # #url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name = 'detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name = 'update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    
   
    
]
