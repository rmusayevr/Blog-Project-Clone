from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                CreateView, UpdateView, DeleteView)

class AboutView(TemplateView):
    template_name = "about.html"

class PostListView(ListView):
    model = Post 

    def get_queryset(self):
        return Post.objects.filter(published_at__lte = timezone.now()).order_by("-published_at")

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = "/accounts/login"
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login"
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

class PostDraftsListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    model = Post 

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull = True).order_by("created_at")


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect("post_detail", pk = pk)

@login_required
def add_comments(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", pk = post.pk)
    else: 
        form = CommentForm()
    return render(request, "post_form.html", {"form":form})

@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("post_detail", pk = post_pk)

@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.approve()
    return redirect("post_detail", pk = comment.post.pk)
