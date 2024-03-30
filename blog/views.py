from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    all_posts = Post.objects.all()
    return render(request, "blog/index.html", {'all_posts': all_posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
