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

from media_app.models import Post
from .serializers import (PostCreateUpdateSerializer,
	PostListSerializer, 
	PostDetailSerializer,
	)

from .permissions import IsOwnerOrReadOnly

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from .pagination import (
	PostLimitOffsetPagination,
	PostPageNumberPagination,
	)


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	#permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)


class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
	pagination_class = PostPageNumberPagination #PageNumberPagination
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):	
		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Post.objects.all()	

		### Serching items 
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains = query) |
				Q(content__icontains = query) |
				Q(user__first_name__icontains = query) |
				Q(user__last_name__icontains = query) 
				).distinct()
		return queryset_list


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug"	# By deafult is pk. IF not set your slug will be ignored, 
							# and goes directly to item without slug.
	permission_classes = [AllowAny]

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = "slug"
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user = self.request.user)


class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	lookup_field = "slug"
	permission_classes = [IsOwnerOrReadOnly]
