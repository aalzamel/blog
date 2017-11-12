from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
	thelist  = Post.objects.all()
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
	}

	return render(request, "post_list.html", context)



# Detailed page of the post

def post_detail(request, post_id):
	#item = Post.objects.get(id=1000)
	item = get_object_or_404(Post, id=post_id)
	context = {
		"items": item,
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
	form = PostForm()
	print(request.method)
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES or None)
		print('if statment is passed')
		if form.is_valid():
			print('form is valid')
			form.save()
			messages.success(request, " Awesome, a blog post has been added")
			return redirect("posts:post_list")
	context = {
		"form": form
	}

	return render(request, "post_create.html", context)



# Updating a post

def post_update(request,post_id):
	item = Post.objects.get(id=post_id)

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

def post_delete(request,post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "Post have been deleted")
	return redirect("posts:post_list")





