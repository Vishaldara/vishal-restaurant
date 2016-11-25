from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post


def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('-published_date')
    return render(request, 'blogposts.html', {'posts': posts})


def post_detail(request, id):
    post  = get_object_or_404(Post, pk=id)
    post.views += 1 # clock up the number of post views
    post.save()
    return render(request, "postdetails.html",{'post': post})