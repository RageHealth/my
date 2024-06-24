from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import PostForm, CommentForm

from members.models import Notification



def index(request):
    all_posts = Post.objects.all()
    items_per_page = 4

    len(all_posts)


    paginator = Paginator(all_posts, items_per_page)

    page_number = request.GET.get('page')
    
    all_posts = paginator.get_page(page_number)

    return render(request, "blog/index.html", {'all_posts': all_posts, 'kol': len(all_posts)})

def post_detail(request, pk):
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post':post,
        'form_comment': form,
        
    }

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=pk)

    return render(request, 'blog/post_detail.html', context)


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

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            existing_like = Like.objects.filter(user=request.user, post=post)

            if request.user != post.author:
                print('notification')
                Notification().add_like(post, request.user)
            
            if not existing_like:
                # Если лайка еще не было, создаем новый
                Like.objects.create(user=request.user, post=post)
                return JsonResponse({'liked': True})
            else:
                # Если лайк уже был поставлен, удаляем его
                existing_like.delete()
                return JsonResponse({'unliked': True})
            

        else:
            return JsonResponse({'error': 'Пользователь не авторизован'}, status=401)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index') 
    form = PostForm(instance=post)

    
    return render(request, 'blog/create_post.html', {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    post.delete()
    return redirect("blog:index") 

def delete_com(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    post = comment.post
    comment.delete()
    return redirect("blog:post_detail", pk=post.id) 

