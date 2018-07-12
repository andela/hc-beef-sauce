from django import forms
from .models import Article


class CreateBlog(forms.ModelForm):
	"""creates a form for a blog post"""

	class Meta:
		model = Article
		fields = ['title', 'body', 'category', 'status']
