import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
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
		if Bookmark.objects.filter(user=self.context['request'].user).filter(url__iexact=validated_data['url']):
			raise serializers.ValidationError('This link is exists')
		try:
			soup = BeautifulSoup(requests.get(validated_data['url']).text, 'html.parser')
		except ConnectionError as e:
			pass

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
		favicon = ''
		try:
			favicon = str(soup.find('link', rel='icon')['href'])
			if not favicon.startswith(url[:4]):
				if '.' not in favicon.split('/')[2]:
					url_s = url.split('/')
					if len(url_s) > 2:
						favicon = url_s[0]+url_s[1]+url_s[2] + favicon
					else:
						favicon = url + favicon
		except TypeError as error:
			pass
				
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