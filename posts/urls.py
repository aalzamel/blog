from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^home/$', views.post, name="newpost"),
	url(r'^list/$', views.post_list, name="post_list"),
	# the below URL format is called RegS - Python Regular Expressions
	url(r'^detail/(?P<post_slug>[-\w]+)/$', views.post_detail, name="detail"),
	url(r'^create/$', views.post_create, name="post_create"),
	url(r'^update/(?P<post_slug>[-\w]+)/$', views.post_update, name="post_update"),
	url(r'^delete/(?P<post_slug>[-\w]+)/$', views.post_delete, name="post_delete"),
	url(r'^like_button/(?P<post_id>\d+)/$', views.like_button, name="like_button"),
    url(r'^signup/$', views.usersignup, name="usersignup"),
    url(r'^login/$', views.userlogin, name="userlogin"),
    url(r'^logout/$', views.userlogout, name="userlogout"),
    url(r'^google/$', views.lmgtfy, name="lmgtfy"),


]
