from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp", "updated"]
	search_fields = ["title", "content"]

	class Meta:
		model = Post



admin.site.register(Post, PostAdmin)

