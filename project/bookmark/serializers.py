from rest_framework import status
from rest_framework import serializers

from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'

    def validate(self, data):
        if Bookmark.objects.filter(user=self.context['request'].user).filter(url__iexact=data['url']):
            raise serializers.ValidationError('This link is exists')
        return data

    def create(self, validated_data):
        bookmark = Bookmark(
            user = self.context['request'].user,
            url = validated_data['url'],
        )
        bookmark.save()
        return bookmark
