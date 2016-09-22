from django.db.models import Q

from rest_framework.generics import (ListAPIView, 
	CreateAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)

from rest_framework.permissions import (AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from comments.models import Comment

from .serializers import (
	CommentListSerializer,
	CommentDetailSerializer,
	create_comment_serializer,
	)

from media_app.api.permissions import IsOwnerOrReadOnly

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from media_app.api.pagination import (
	PostLimitOffsetPagination,
	PostPageNumberPagination,
	)

from rest_framework.mixins import (
	DestroyModelMixin, 
	UpdateModelMixin,
	)


class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	#serializer_class = PostCreateUpdateSerializer
	#permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		model_type = self.request.GET.get('type')	# "type" is what ever it is posts, lectures, videos...
		slug = self.request.GET.get('slug')
		parent_id = self.request.GET.get('parent_id', None)		# None is default value

		return create_comment_serializer(
			model_type = model_type, 
			slug = slug, 
			parent_id = parent_id, 
			user = self.request.user)

	# def perform_create(self, serializer):
	# 	serializer.save(user = self.request.user)

class CommentListAPIView(ListAPIView):
	serializer_class = CommentListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['content', 'user__first_name', 'user__last_name']
	pagination_class = PostPageNumberPagination #PageNumberPagination
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):	
		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Comment.objects.filter(id__gte = 0)

		### Serching items 
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains = query) |
				Q(user__first_name__icontains = query) |
				Q(user__last_name__icontains = query) 
				).distinct()
		return queryset_list

# Combining Detail & Edit in one place
# class CommentEditAPIView(RetrieveAPIView):
# 	queryset = Comment.objects.all()
# 	serializer_class = CommentDetailSerializer
# 	# lookup_field = "slug"		# By deafult is pk. IF not set your slug will be ignored, 
# 								# and goes directly to item without slug.


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte = 0) 	# To be able to edit both parent, child. 
													# We do this because we rewritten all() method
	serializer_class = CommentDetailSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)










# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 	def perform_update(self, serializer):
# 		serializer.save(user = self.request.user)


# class PostDeleteAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostListSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
