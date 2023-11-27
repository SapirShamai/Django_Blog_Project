from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def home(request):
    """View for rendering the home page of the blog."""

    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    """View for displaying a list of blog posts."""

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 8


class UserPostListView(ListView):
    """View for displaying a list of blog posts by a specific user."""

    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    """View for displaying details of a single blog post."""

    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new blog post."""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing blog post."""

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting an existing blog post."""
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    """View for rendering the about page of the blog."""

    return render(request, 'blog/about.html', {'title': 'About'})
