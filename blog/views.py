from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Comment, Category, Tag
from .forms import PostForm, CommentForm, CustomUserCreationForm


# Function-Based Views

def post_list(request):
    """Display list of published posts with search and filtering"""
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Category filtering
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # Tag filtering
    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for sidebar
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_tag': tag_id,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    """Display single post with comments"""
    post = get_object_or_404(Post, pk=pk, status='published')
    comments = post.comments.filter(is_active=True).select_related('author')
    
    # Handle comment form submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """Create new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create New Post'})


@login_required
def post_update(request, pk):
    """Update existing blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post', 'post': post})


@login_required
def post_delete(request, pk):
    """Delete blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our blog!')
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


# Class-Based Views

class CategoryPostListView(ListView):
    """List posts by category"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(
            category=self.category,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    """List posts by tag"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return Post.objects.filter(
            tags=self.tag,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class UserPostListView(ListView):
    """List posts by specific user"""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        from django.contrib.auth.models import User
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(
            author=self.author,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

