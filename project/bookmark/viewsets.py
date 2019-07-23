from rest_framework import viewsets

from .models import Bookmark
from .serializers import BookmarkSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
	serializer_class = BookmarkSerializer

	def get_queryset(self):
		return Bookmark.objects.filter(user__id=self.request.user.id)