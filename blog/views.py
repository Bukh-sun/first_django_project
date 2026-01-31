from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import CommentForm


def post_list(request):
    """List of all published posts"""

    posts = models.Post.published.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """Post detail view"""

    post = get_object_or_404(models.Post.objects, pk=pk)
    post.increment_views()

    comments = post.comments.all().order_by('-created_date')
    comment_form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    previous_post = models.Post.published.filter(
        published_date__lt=post.published_date
    ).order_by('-published_date').first()

    next_post = models.Post.published.filter(
        published_date__gt=post.published_date
    ).order_by('published_date').first()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'previous_post': previous_post,
        'next_post': next_post,
    })

def category_list(request, category_id):
    """Posts of the chosen category"""

    category = get_object_or_404(models.Category, pk=category_id)
    posts = models.Post.published.filter(category=category).order_by('-published_date')
    return render(request, 'blog/category_list.html', {'category': category, 'posts': posts})