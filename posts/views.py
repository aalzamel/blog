from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404
from django.utils import timezone
from django.db.models import Q

# Test post model

def post(request):
	context = {
		"firstname": "Aziz",
		"lastname": "Alzamel",
		"auser": request.user.username,
	}

	return render(request, "home.html", context)



# List view of the blog posts

def post_list(request):
	# To apply ordering on a view level
	# thelist  = Post.objects.all().order_by('id', '-title')
	today = timezone.now()



	if request.user.is_staff:
		thelist  = Post.objects.all()
	else:
		thelist = Post.objects.filter(draft=False, publish_date__lte=today)

	query = request.GET.get('q')
	if query:
		thelist = thelist.filter(
		Q(title__icontains=query)|
        Q(content__icontains=query)|
        Q(author__first_name__icontains=query)|
        Q(author__last_name__icontains=query)
		).distinct()


	paginator = Paginator(thelist, 9)




	page = request.GET.get('page')
	try:
		thelist = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		thelist = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		thelist = paginator.page(paginator.num_pages)

	context = {
		"post_items": thelist,
		"today": today,
	}

	return render(request, "post_list.html", context)



# Detailed page of the post

def post_detail(request, post_slug):
	item = get_object_or_404(Post, slug=post_slug)

	if not request.user.is_staff:
		if item.draft or item.publish_date > timezone.now():
			raise Http404
	#item = Post.objects.get(id=1000)
	context = {
		"items": item,
		"share_string": quote(item.content),
	}

	return render(request, "detail.html", context)



# def post_create(request):
# 	form = PostForm(request.POST or None, request.FILES or None)
# 	if form.is_valid():
# 		form.save()
# 		return redirect("posts:post_list")
# 	context = {
# 		"form": form
# 	}

# 	return render(request, "post_create.html", context)



# Creating a post

def post_create(request):
	if not request.user.is_authenticated():
		raise Http404	
	form = PostForm()
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = request.user
			item.save()

			messages.success(request, " Awesome, a blog post has been added")
			return redirect("posts:post_list")
	context = {
		"form": form
	}

	return render(request, "post_create.html", context)



# Updating a post

def post_update(request,post_slug):
	
	item = Post.objects.get(slug=post_slug)

	if request.user != item.author and not request.user.is_staff:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None, instance=item)

	if form.is_valid():
		form.save()
		messages.info(request, "Blog post updated")
		return redirect("posts:post_list")
	
	context = {
		"form": form,
		"item": item,
	}

	return render(request, "post_update.html", context)


# Deleting a post

def post_delete(request,post_slug):
	if not request.user.is_staff:
		raise Http404
	Post.objects.get(slug=post_slug).delete()
	messages.warning(request, "Post have been deleted")
	return redirect("posts:post_list")





