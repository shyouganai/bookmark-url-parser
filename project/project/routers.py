from rest_framework import routers
from bookmark.viewsets import BookmarkViewSet

router = routers.DefaultRouter()

router.register(r'bookmark', BookmarkViewSet, basename='bookmark')