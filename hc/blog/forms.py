from django import forms
from .models import Article


class CreateBlog(forms.ModelForm):
	"""creates a form for a blog post"""

	class Meta:
		model = Article
		fields = ['title', 'body', 'category', 'status', 'tags']
		widgets = {
			'title': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			'body': forms.Textarea(
				attrs={
					'class': 'form-control'
				}
			),
			'category': forms.Select(
				attrs={
					'class': 'form-control'
				}
			),
			'status': forms.Select(
				attrs={
					'class': 'form-control'
				}
			)
		}
