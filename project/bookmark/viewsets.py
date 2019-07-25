from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Bookmark
from .serializers import BookmarkSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
	serializer_class = BookmarkSerializer

	def get_queryset(self):
		return Bookmark.objects.filter(
			user__id=self.request.user.id).order_by(
			'-id')