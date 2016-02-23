from django.conf.urls import patterns
from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    # url('^about$', views.about, name='about'),
    # url('^category/(?P<category_name_slug>[\w\-]+)/?$', views.category, name='category'),
]
