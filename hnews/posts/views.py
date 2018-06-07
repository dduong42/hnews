import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    template_name = 'posts/list.html'
    model = Post
    context_object_name = 'posts'


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
