from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

from .forms import PostForm

def index(request):
    all_posts = Post.objects.all()
    return render(request, "blog/index.html", {'all_posts': all_posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index') 
    form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})
