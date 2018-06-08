import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    template_name = 'posts/list.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['posts'] = json.dumps([
            {
                'title': post.title,
                'how_long_ago': post.how_long_ago(),
                'domain_name': post.get_domain_name(),
                'upvoted': post.upvotes.filter(user=self.request.user).count() > 0,
                'upvote_url': reverse('posts:set_upvoted_post', kwargs={'post_id': post.id}),
            }
            for post in context['posts']
        ])
        return context


@require_POST
@login_required
def set_upvoted_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        upvoted = json.loads(request.body.decode('utf-8'))['upvoted']
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    post.set_upvoted(request.user, upvoted=upvoted)
    # 204: No content
    return HttpResponse(status=204)
