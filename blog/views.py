from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .form import PostForm
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


class post_listAPI(APIView):
    def get(self,request,*args,**kwargs):
        authors = User.objects.all()
        if(request.GET.__contains__('author')):
            name = request.GET['author']
        else:
            name = 'All'

        if(name=='All'):
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        else:
            author_id = get_object_or_404(User,username=name)
            posts = Post.objects.filter(author = author_id).order_by('published_date')

        return render(request, 'blog/post_list.html', {'posts': posts,'authors':authors})

post_list = post_listAPI.as_view()
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
