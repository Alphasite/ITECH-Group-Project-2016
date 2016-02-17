from django.conf.urls import patterns
from django.conf.urls import url

from game import views

urlpatterns = patterns(
    '',
    url('^$', views.index, name='index'),
    url('^$', views.index, name='register')
    # url('^about$', views.about, name='about'),
    # url('^category/(?P<category_name_slug>[\w\-]+)/?$', views.category, name='category'),
)
