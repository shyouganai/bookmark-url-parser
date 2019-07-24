import requests
from rest_framework import serializers
from bs4 import BeautifulSoup

from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bookmark
		fields = '__all__'

	def validate(self, data):
		return data

	def create(self, validated_data):
		soup = BeautifulSoup(requests.get(validated_data['url']).text, 'html.parser')

		# Title
		title = soup.title.string

		# Description
		for tag in soup.find_all('meta'):
			if tag.get('name') and tag.get('name').lower() == 'description':
				description = tag.get('content')
				break
		else:
			description = 'Нет информации...'

		# Url
		url = validated_data['url']

		# Favicon
		favicon = str(soup.find('link', rel='icon')['href'])

		if favicon.startswith('/'):
			url_s = url.split('/')
			if len(url_s) > 2:
				favicon = url_s[0]+url_s[1]+url_s[2] + favicon
			else:
				favicon = url + favicon
				
		# Create Bookmark
		bookmark = Bookmark(
			user = self.context['request'].user,
			title = title,
			description = description,
			url = url,
			favicon = favicon
		)
		# Save new Bookmark
		bookmark.save()
		return bookmark