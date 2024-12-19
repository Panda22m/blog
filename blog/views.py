from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # 해당 게시물의 모든 댓글 가져오기

    # 세션에서 좋아요 수 가져오기, 없으면 0으로 초기화
    likes = request.session.get(f'likes_{post.pk}', 0)

    if request.method == "POST":
        if 'like' in request.POST:
            likes += 1
            request.session[f'likes_{post.pk}'] = likes  # 세션에 좋아요 수 저장
            return redirect('post_detail', pk=post.pk)  # 좋아요 후 페이지 새로 고침
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user  # 현재 로그인한 사용자 설정
                comment.save()
                return redirect('post_detail', pk=post.pk)  # 댓글 작성 후 게시물 상세 페이지로 리다이렉트
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'likes': likes,  # 좋아요 수 전달
    })

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')  # 삭제 후 게시물 목록으로 리다이렉트
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 회원가입 후 로그인 페이지로 리다이렉트
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})