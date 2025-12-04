from django.shortcuts import render, get_object_or_404
from . import models

def post_list(request):
    """List of all published posts"""

    posts = models.Post.published.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """Post detail view"""

    post = get_object_or_404(models.Post.objects, pk=pk)
    post.increment_views()

    return render(request, 'blog/post_detail.html', {'post': post})

def category_list(request, category_id):
    """Posts of the chosen category"""

    category = get_object_or_404(models.Category, pk=category_id)
    posts = models.Post.published.filter(category=category).order_by('-published_date')
    return render(request, 'blog/category_list.html', {'category': category, 'posts': posts})