#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from django.utils import timezone
from django.utils.text import slugify

def create_sample_data():
    print("Creating sample data...")
    
    # Create categories
    categories_data = [
        {'name': 'Technology', 'description': 'Latest trends in technology and programming'},
        {'name': 'Travel', 'description': 'Travel experiences and destination guides'},
        {'name': 'Food', 'description': 'Recipes, restaurant reviews, and culinary adventures'},
        {'name': 'Lifestyle', 'description': 'Tips for better living and personal development'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Create tags
    tags_data = ['python', 'django', 'web-development', 'travel', 'photography', 
                 'cooking', 'health', 'productivity', 'tutorial', 'review']
    
    tags = []
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
        if created:
            print(f"Created tag: {tag.name}")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create sample posts
    posts_data = [
        {
            'title': 'Getting Started with Django: A Comprehensive Guide',
            'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

In this comprehensive guide, we'll explore the fundamentals of Django and walk through building your first web application. Django follows the Model-View-Template (MVT) architectural pattern, which is similar to the more commonly known Model-View-Controller (MVC) pattern.

## Why Choose Django?

Django comes with many built-in features that make web development faster and more secure:

- **Admin Interface**: Django automatically generates an admin interface for your models
- **ORM**: Object-Relational Mapping that lets you interact with your database using Python code
- **Security**: Built-in protection against common security threats
- **Scalability**: Used by major websites like Instagram, Pinterest, and Mozilla

## Setting Up Your First Django Project

To get started with Django, you'll need Python installed on your system. Then you can install Django using pip:

```bash
pip install django
```

Once installed, you can create a new Django project:

```bash
django-admin startproject myproject
```

This creates a new directory with the basic Django project structure. Navigate to your project directory and run the development server:

```bash
cd myproject
python manage.py runserver
```

## Understanding Django Models

Models in Django are Python classes that define the structure of your database tables. Each model class represents a database table, and each attribute represents a database field.

Here's an example of a simple blog post model:

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

## Creating Views and Templates

Views in Django are Python functions or classes that receive web requests and return web responses. Templates are HTML files that define how your data is presented to users.

This is just the beginning of your Django journey. As you continue learning, you'll discover the power and flexibility that Django offers for building robust web applications.''',
            'excerpt': 'Learn the fundamentals of Django web framework and build your first web application with this comprehensive beginner guide.',
            'category': categories[0],  # Technology
            'tags': [tags[0], tags[1], tags[2], tags[8]],  # python, django, web-development, tutorial
            'status': 'published'
        },
        {
            'title': 'Hidden Gems of Southeast Asia: Off the Beaten Path',
            'content': '''Southeast Asia is renowned for its popular destinations like Bangkok, Bali, and Singapore. However, the region is filled with countless hidden gems that offer authentic experiences away from the crowds. In this post, we'll explore some lesser-known destinations that should be on every traveler's bucket list.

## Luang Prabang, Laos

Nestled in the mountains of northern Laos, Luang Prabang is a UNESCO World Heritage site that perfectly blends French colonial architecture with traditional Lao culture. The city is famous for its stunning temples, vibrant night markets, and the daily alms-giving ceremony at dawn.

**What to do:**
- Visit the magnificent Wat Xieng Thong temple
- Climb Mount Phousi for panoramic views of the city
- Take a boat trip to the Pak Ou Caves
- Experience the Kuang Si Falls

## Hoi An, Vietnam

While not entirely unknown, Hoi An remains one of Vietnam's most charming destinations. This ancient trading port features well-preserved architecture, lantern-lit streets, and some of the best food in Southeast Asia.

The city is particularly magical in the evening when thousands of colorful lanterns illuminate the streets and reflect in the Thu Bon River. Don't miss the monthly Full Moon Festival when the entire old town is lit only by traditional lanterns.

## Raja Ampat, Indonesia

For diving enthusiasts, Raja Ampat in West Papua is considered one of the world's best diving destinations. This remote archipelago is home to the richest marine biodiversity on Earth, with over 1,500 species of fish and 600 species of coral.

The name "Raja Ampat" means "Four Kings" in Indonesian, referring to the four main islands: Misool, Salawati, Batanta, and Waigeo. The area is still relatively untouched by mass tourism, making it perfect for those seeking pristine underwater experiences.

## Practical Tips for Exploring Hidden Gems

1. **Research visa requirements** - Some remote destinations may have different entry requirements
2. **Pack appropriately** - Remote areas may have limited shopping options
3. **Learn basic local phrases** - English may not be widely spoken in off-the-beaten-path locations
4. **Respect local customs** - Take time to understand and respect local traditions
5. **Travel insurance** - Essential when visiting remote areas with limited medical facilities

These hidden gems offer incredible experiences for those willing to venture beyond the typical tourist trail. Each destination provides unique insights into local culture, stunning natural beauty, and memories that will last a lifetime.''',
            'excerpt': 'Discover amazing hidden destinations in Southeast Asia that offer authentic experiences away from the tourist crowds.',
            'category': categories[1],  # Travel
            'tags': [tags[3], tags[4]],  # travel, photography
            'status': 'published'
        },
        {
            'title': 'The Art of Homemade Pasta: From Flour to Fork',
            'content': '''There's something magical about making pasta from scratch. The simple combination of flour, eggs, and a pinch of salt transforms into silky ribbons of deliciousness that no store-bought pasta can match. Today, we'll dive into the art of homemade pasta making.

## The Basic Pasta Dough

The foundation of great pasta is the dough. Here's what you'll need:

**Ingredients:**
- 2 cups all-purpose flour (plus extra for dusting)
- 3 large eggs
- 1 tablespoon olive oil
- 1 teaspoon salt

**Instructions:**

1. Create a well with the flour on a clean work surface
2. Crack the eggs into the center and add olive oil and salt
3. Using a fork, gradually incorporate the flour into the eggs
4. Once a shaggy dough forms, knead for 8-10 minutes until smooth
5. Wrap in plastic and rest for at least 30 minutes

## Rolling and Shaping

The key to perfect pasta is achieving the right thickness. If you have a pasta machine, start with the widest setting and gradually work your way to thinner settings. For hand-rolling, use a long rolling pin and work from the center outward.

### Popular Pasta Shapes to Try:

**Fettuccine**: Roll the dough thin and cut into ¼-inch strips. Perfect with creamy sauces.

**Pappardelle**: Similar to fettuccine but cut into wider strips (about ¾-inch). Excellent with hearty meat sauces.

**Ravioli**: Roll thin sheets, add filling, and seal with egg wash. The possibilities for fillings are endless.

**Orecchiette**: Hand-formed "little ears" that are perfect for catching chunky sauces.

## Cooking Fresh Pasta

Fresh pasta cooks much faster than dried pasta - usually in just 2-4 minutes. The water should be at a rolling boil with plenty of salt (it should taste like seawater). Fresh pasta is done when it floats to the surface and has a tender but still slightly firm texture.

## Sauce Pairing Tips

- **Light sauces** (olive oil, butter, herbs) pair well with delicate pasta shapes
- **Cream sauces** work beautifully with fettuccine and pappardelle
- **Chunky sauces** are perfect for shapes that can hold the sauce like orecchiette
- **Simple tomato sauces** complement almost any pasta shape

## Storage and Make-Ahead Tips

Fresh pasta can be stored in the refrigerator for up to 2 days or frozen for up to 3 months. To freeze, lay the pasta on a baking sheet until frozen solid, then transfer to freezer bags.

Making pasta from scratch is a rewarding experience that connects us to centuries of culinary tradition. With practice, you'll develop a feel for the dough and discover your own favorite combinations of shapes and sauces.''',
            'excerpt': 'Master the art of making fresh pasta from scratch with this detailed guide covering dough preparation, shaping techniques, and sauce pairings.',
            'category': categories[2],  # Food
            'tags': [tags[5], tags[8]],  # cooking, tutorial
            'status': 'published'
        },
        {
            'title': '10 Productivity Hacks That Actually Work',
            'content': '''In our fast-paced world, productivity has become the holy grail of personal and professional success. While there are countless productivity tips floating around the internet, not all of them are practical or effective. Here are 10 productivity hacks that have been tested and proven to work.

## 1. The Two-Minute Rule

If a task takes less than two minutes to complete, do it immediately rather than adding it to your to-do list. This simple rule prevents small tasks from accumulating and becoming overwhelming.

## 2. Time Blocking

Instead of keeping a simple to-do list, assign specific time blocks to your tasks. This method helps you estimate how long tasks actually take and prevents overcommitting your schedule.

## 3. The Pomodoro Technique

Work in focused 25-minute intervals followed by 5-minute breaks. After four pomodoros, take a longer 15-30 minute break. This technique helps maintain focus and prevents burnout.

## 4. Batch Similar Tasks

Group similar activities together and complete them in one session. For example, respond to all emails at designated times rather than checking throughout the day.

## 5. The 80/20 Rule (Pareto Principle)

Focus on the 20% of tasks that produce 80% of your results. Identify your high-impact activities and prioritize them over busy work.

## 6. Digital Minimalism

Reduce digital distractions by:
- Turning off non-essential notifications
- Using website blockers during focused work time
- Keeping your phone in another room while working
- Unsubscribing from unnecessary email lists

## 7. The "Eat the Frog" Method

Tackle your most challenging or important task first thing in the morning when your energy and willpower are at their peak.

## 8. Weekly Reviews

Spend 30 minutes each week reviewing what you accomplished, what didn't work, and planning for the upcoming week. This helps you stay aligned with your goals and continuously improve your systems.

## 9. Energy Management

Pay attention to your natural energy rhythms and schedule demanding tasks during your peak hours. For most people, this is in the morning, but everyone is different.

## 10. The "Good Enough" Principle

Perfectionism is the enemy of productivity. Learn to recognize when something is good enough and move on. You can always improve it later if needed.

## Implementation Tips

- Start with one or two techniques rather than trying to implement everything at once
- Give each method at least two weeks before deciding if it works for you
- Customize these techniques to fit your specific situation and work style
- Remember that productivity is about working smarter, not harder

The key to lasting productivity improvement is finding the methods that work best for your personality, work style, and life circumstances. Experiment with these techniques and adapt them to create your own personalized productivity system.''',
            'excerpt': 'Discover 10 proven productivity techniques that can help you work smarter, manage your time better, and achieve more with less stress.',
            'category': categories[3],  # Lifestyle
            'tags': [tags[7], tags[8]],  # productivity, tutorial
            'status': 'published'
        }
    ]
    
    # Create posts
    for i, post_data in enumerate(posts_data):
        slug = slugify(post_data['title'])
        post, created = Post.objects.get_or_create(
            slug=slug,
            defaults={
                'title': post_data['title'],
                'content': post_data['content'],
                'excerpt': post_data['excerpt'],
                'author': admin_user,
                'category': post_data['category'],
                'status': post_data['status'],
                'published_at': timezone.now()
            }
        )
        
        if created:
            # Add tags
            post.tags.set(post_data['tags'])
            print(f"Created post: {post.title}")
            
            # Create sample comments
            comment_content = [
                "Great article! Very informative and well-written.",
                "Thanks for sharing this. I learned a lot from your post.",
                "Excellent tips! I'll definitely try implementing these.",
                "This is exactly what I was looking for. Thank you!"
            ]
            
            for j, content in enumerate(comment_content[:2]):  # Add 2 comments per post
                Comment.objects.create(
                    post=post,
                    author=admin_user,
                    content=content,
                    is_active=True
                )
    
    print("Sample data created successfully!")
    print(f"Created {Category.objects.count()} categories")
    print(f"Created {Tag.objects.count()} tags")
    print(f"Created {Post.objects.count()} posts")
    print(f"Created {Comment.objects.count()} comments")

if __name__ == '__main__':
    create_sample_data()

