from django.conf.urls import url
from . import views

app_name = 'articles'

urlpatterns = [
	url(r'^$', views.article_list, name='list'),
	url(r'^create/$', views.create_post, name='create'),
	url(r'^category-detail/(?P<slug>[\w-]+)/$', views.category_detail, name='category_detail'),
	url(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='detail')

]
