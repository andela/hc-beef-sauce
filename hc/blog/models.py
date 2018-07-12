from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Category(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class Article(models.Model):
	STATUS_CHOICES = (
		("Published", "Published"),
		("Draft", "Draft")
	)
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	body = models.TextField()
	author = models.ForeignKey(User, default=None)
	category = models.ForeignKey(Category, default=None)
	status = models.CharField(max_length=15, default='Draft', choices=STATUS_CHOICES)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# thumbnail = models.ImageField(default='default.png', blank=True)

	def __str__(self):
		return self.title

	def snippet(self):
		return self.body[:50] + "..."

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Article, self).save(*args, **kwargs)
