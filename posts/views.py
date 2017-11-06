from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post(request):
	context = {
	"firstname": "Aziz",
	"lastname": "Alzamel",
	"auser": request.user.username,
	}

	return render(request, "home.html", context)


def post_list(request):
	thelist  = Post.objects.all()
	context = {
	"post_items": thelist,
	}

	return render(request, "post_list.html", context)


def post_detail(request, post_id):
	#item = Post.objects.get(id=1000)
	item = get_object_or_404(Post, id=post_id)
	context = {
	"items": item,
	}

	return render(request, "detail.html", context)
