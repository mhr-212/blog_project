from django.contrib import admin
from .models import Post, Comment, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['tags']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'image')
        }),
        ('Categorization', {
            'fields': ('tags',)
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'content')
        }),
        ('Moderation', {
            'fields': ('is_active',)
        }),
    )

