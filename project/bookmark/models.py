from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from .tasks import add_bookmark

class Bookmark(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
		null=False, blank=True, verbose_name='Владелец')
	title = models.CharField(max_length=100, null=False, blank=True,
		verbose_name='Заголовок')
	description = models.TextField(null=False, blank=True,
		verbose_name='Описание')
	url = models.URLField(max_length=500, null=False, blank=False)
	favicon = models.CharField(max_length=500, null=True, blank=True)

	def get_absolute_url(self):
		return reverse('bookmark-detail', args=[str(self.id)])

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Закладка'
		verbose_name_plural = 'Закладки'

def bookmark_post_save(sender, instance, signal, *args, **kwargs):
    add_bookmark.delay(instance.id)

signals.post_save.connect(bookmark_post_save, sender=Bookmark)
