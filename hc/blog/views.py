from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import forms


def article_list(request):
	"""lists all blogs"""
	articles = Article.objects.filter(status='Published')
	return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug):
	"""handles a single blog post"""
	article = get_object_or_404(Article, slug=slug)
	return render(request, 'blog/article_detail.html', {'article': article})


def category_detail(request, slug):
	category = get_object_or_404(Category, slug=slug)
	article = Article.objects.filter(category=category)
	context = {
		'category': category,
		'article': article
	}
	return render(request, 'blog/category_detail.html', context)


@login_required()
def create_post(request):
	"""handles creation of a blog post"""
	if request.method == 'POST':
		form = forms.CreateBlog(request.POST)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return redirect('articles:list')
	else:
		form = forms.CreateBlog()
	return render(request, 'blog/create_post.html', {'form': form})