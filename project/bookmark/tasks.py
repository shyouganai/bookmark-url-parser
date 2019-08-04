import requests
import logging
from bs4 import BeautifulSoup
from project.celery import app
from . import models

@app.task
def add_bookmark(bookmark_id):
    bookmark = models.Bookmark.objects.get(pk=bookmark_id)
    try:
        soup = BeautifulSoup(requests.get(bookmark.url).text, 'html.parser')
    except ConnectionError as e:
        logging.warning('Connection Error')
        return

    # Title
    title = soup.title.string

    # Description
    for tag in soup.find_all('meta'):
        if tag.get('name') and tag.get('name').lower() == 'description':
            description = tag.get('content')
            break
    else:
        description = 'Нет информации...'

    # Favicon
    favicon = ''
    try:
        favicon = str(soup.find('link', rel='icon')['href'])
        if not favicon.startswith(bookmark.url[:4]):
            if '.' not in favicon.split('/')[2]:
                url_s = bookmark.url.split('/')
                if len(url_s) > 2:
                    favicon = url_s[0]+url_s[1]+url_s[2] + favicon
                else:
                    favicon = bookmark.url + favicon
    except TypeError as error:
        pass

    bookmark.title = title
    bookmark.description = description
    bookmark.favicon = favicon
    bookmark.save()
