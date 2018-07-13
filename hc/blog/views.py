from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from . import forms
from taggit.models import Tag


def article_list(request, tag_slug=None):
	"""lists all blogs"""
	articles = Article.objects.filter(status='Published').order_by('-updated')
	all_tags = Article.tags.all()
	categories = Category.objects.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		articles = articles.filter(tags__in=[tag])
	paginator = Paginator(articles, 10)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	context = {
		'articles': items,
		'tags': tag,
		'all_tags': all_tags,
		'all_categories': categories
	}

	return render(request, 'blog/article_list.html', context)


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
			form.save_m2m()
			return redirect('articles:list')
	else:
		form = forms.CreateBlog()
	return render(request, 'blog/create_post.html', {'form': form})


def edit_post(request, pk):
	post = get_object_or_404(Article, pk=pk)

	if request.method == 'POST':
		form = forms.CreateBlog(request.POST, instance=post)

		try:
			if form.is_valid():
				form.save()
				messages.success(request, 'Your post has been updated')
		except Exception as e:
			messages.warning(request, f'Your post was not saved due to an error: {e}')

	else:
		form = forms.CreateBlog()

	context = {
		'form': form,
		'post': post
	}
	render(request, 'blog/create_post.html', context)


def search(request):
	query = request.GET.get('q')
	results = Article.objects.filter(Q(title__icontains=query))
