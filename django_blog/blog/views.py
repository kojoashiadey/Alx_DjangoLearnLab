from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.db.models import Q

from .forms import UserRegisterForm, PostForm, CommentForm
from .models import Post, Comment, Tag


# ==============================
# User Authentication Views
# ==============================

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registering
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """Display user profile page."""
    return render(request, 'blog/profile.html')


class CustomLoginView(LoginView):
    """Custom login view using Django’s built-in LoginView."""
    template_name = 'blog/login.html'


class CustomLogoutView(LogoutView):
    """Custom logout view using Django’s built-in LogoutView."""
    template_name = 'blog/logout.html'


# ==============================
# Blog Post CRUD Views
# ==============================

class PostListView(ListView):
    """List all blog posts."""
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]


class PostDetailView(DetailView):
    """Show details of a single post with comment form."""
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow logged-in users to create a new post (with tags)."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Handle tags
        tags_str = form.cleaned_data.get('tags', '')
        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                self.object.tags.add(tag_obj)
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow only the author to update their post (with tags)."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill tags as comma-separated list
        initial['tags'] = ', '.join(tag.name for tag in self.get_object().tags.all())
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Update tags: clear existing then re-add
        tags_str = form.cleaned_data.get('tags', '')
        self.object.tags.clear()
        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                self.object.tags.add(tag_obj)
        return response

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow only the author to delete their post."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        return self.request.user == self.get_object().author


# ==============================
# Comment CRUD Views
# ==============================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Allow logged-in users to comment on a post."""
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        # Changed post_pk → pk to match the URL
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow only the author to edit their comment."""
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow only the author to delete their comment."""
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


# ==============================
# Tag + Search Views
# ==============================

class PostByTagListView(ListView):
    """List posts filtered by a specific tag slug."""
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs.get('tag_slug')
        return context


class SearchResultsView(ListView):
    """List posts filtered by a search query (title, content, tags)."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
