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

from .serializers import (
	UserCreateSerializer,
	UserLoginSerializer
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

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	queryset = User.objects.all()
	permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer


	def post(self, request, *args, **kwargs):
		data = request.data	# data comes from rest built in
		serializer = UserLoginSerializer(data = data)
		if serializer.is_valid(raise_exception = True):
			new_data = serializer.data
			return Response(new_data, status = HTTP_200_OK)	# rest_framework Response, not Django HttpResponse
		return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)

	