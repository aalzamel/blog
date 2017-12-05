from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^comments/', include('django_comments.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^posts/', include('posts.urls', namespace="posts")),
	url(r'^googly/', include('googly.urls', namespace="googly")),
    url(r'^gitty/', include('gitty.urls', namespace="gitty")),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/', include('api.urls', namespace='api')),

]


if settings.DEBUG:
	urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)