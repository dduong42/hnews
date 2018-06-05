from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    template_name = 'posts/list.html'
    model = Post
    context_object_name = 'posts'
