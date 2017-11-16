from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Post(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(User, default=1)
	slug = models.SlugField(unique=True)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	draft = models.BooleanField(default=False)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(null=True, blank=True, upload_to="post_images")
	
	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"post_slug":self.slug})

	# Add global ordering to the Post model

	class Meta:
		ordering = ['id']

def create_slug(instance, new_slug=None):
	slug_value = slugify(instance.title)
	if new_slug is not None:
		slug_value = new_slug
		query = Post.objects.filter(slug=slug_value)
		print(query)
		if query.exists():
			slug_value = "%s-%s"%(slug_value, query.last().id)
			return create_slug(instance, new_slug=slug_value)
	return slug_value

def pre_save_post_receiver(*args, **kwargs):
	instance = kwargs['instance']
#	print(instance.title,instance.slug)
	if instance.slug:
		x = slugify(instance.title)
		instance.slug = create_slug(instance, new_slug=x)
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)


