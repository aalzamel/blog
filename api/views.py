from posts.models import Post
from .permissions import IsAuthor
from .serializers import UserLoginSerializer, UserCreateSerializer, PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, CommentListSerializer, CommentCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.db.models import Q
from rest_framework.filters import SearchFilter
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone 
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

class UserLoginView(APIView):
	permission_classes = [AllowAny,]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserCreateView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer


class CommentListView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get("query")
		if query:
			queryset = queryset.filter(
					Q(object_pk=query)|
					Q(user=query)
				).distinct()
		return queryset


class CommentCreateView(CreateAPIView):

	queryset = Post.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(
			content_type = ContentType.objects.get_for_model(Post),
			site=Site.objects.get(id=1),
			user=self.request.user,
			user_name=self.request.user.username,
			submit_date=timezone.now(),
			)


class PostListView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['title', 'content', 'author__username']
	permission_classes = [AllowAny,]
	def get_queryset(self, *args, **kwargs):
		queryset = Post.objects.all()
		query = self.request.GET.get("query")
		if query:
			queryset = queryset.filter(
					Q(title__icontains=query)|
					Q(content__icontains=query)

				).distinct()
		return queryset




class PostDetailView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [AllowAny,]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class PostDeleteView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [IsAuthenticated, IsAuthor,]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'


class PostUpdateView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated, IsAuthor,]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'


class PostCreateView(CreateAPIView):

	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

