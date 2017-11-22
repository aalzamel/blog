from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate

def usersignup(request):
	context = {}
	form = UserSignUp()
	context['form'] = form

	if request.method == "POST":
		form = UserSignUp(request.POST)

		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()
			auth = authenticate(username=username, password=password)
			login(request, auth)
			return redirect("posts:post_list")
		messages.warning(request, form.errors)
		return redirect("posts:signup")
	return render(request, "signup.html", context)



#login form

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form

	if request.method == "POST":
		form = UserLogin(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth = authenticate(username=username, password=password)
			if auth is not None:
				login(request, auth)
				return redirect("posts:post_list")
			messages.warning (request, 'Incorrect username/password combination')
			return redirect("posts:userlogin")
		messages.warning(request, form.errors)
		return redirect("posts:userlogin")
	return render(request, "login.html", context)



def userlogout(request):
	logout(request)
	return redirect("posts:post_list")
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
	liked = False
	if request.user.is_authenticated():
		if Like.objects.filter(post=item, user=request.user).exists():
			liked = True
		else:
			liked = False

	#like_count = Like.objects.filter(post=item).count()
	# another way of doing the above line is:
	like_count = item.like_set.count()

	#item = Post.objects.get(id=1000)
	context = {
		"items": item,
		"share_string": quote(item.content),
		"liked": liked,
		"like_count": like_count,
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

# def lmgtfy(request):
# 	base = "http://lmgtfy.com/?q="
# 	search = ""

# 	thelink = base+search

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



def like_button(request, post_id):
	post_object = Post.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user, post=post_object)

	if created:
		action = "like"
	else:
		like.delete()
		action = "unlike"

	like_count = post_object.like_set.count()

	response = {
		"action": action,
		"like_count": like_count,
	}

	return JsonResponse(response, safe=False)