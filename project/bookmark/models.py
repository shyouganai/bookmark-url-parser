from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE,
		null=False, blank=True, verbose_name='Владелец')
	title = models.CharField(max_length=100, null=False, blank=True,
		verbose_name='Заголовок')
	description = models.TextField(null=False, blank=True,
		verbose_name='Описание')
	url = models.CharField(max_length=1000, null=False, blank=False)
	favicon = models.CharField(max_length=1000, null=True, blank=False)

	def get_absolute_url(self):
		return reverse('bookmark-detail', args=[str(self.id)])

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Закладка'
		verbose_name_plural = 'Закладки'