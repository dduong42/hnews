from datetime import timedelta
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import pluralize
from django.utils import timezone
from django.urls import reverse


class HowLongAgoMixin:
    def how_long_ago(self):
        how_long = timezone.now() - self.creation_date
        if how_long < timedelta(minutes=1):
            return f'{how_long.seconds} second{pluralize(how_long.seconds)} ago'
        elif how_long < timedelta(hours=1):
            # total_seconds returns a float
            minutes = int(how_long.total_seconds()) // 60
            return f'{minutes} minute{pluralize(minutes)} ago'
        elif how_long < timedelta(days=1):
            hours = int(how_long.total_seconds()) // 3600
            return f'{hours} hour{pluralize(hours)} ago'
        else:
            return f'{how_long.days} day{pluralize(how_long.days)} ago'


class Post(models.Model, HowLongAgoMixin):
    creator = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    title = models.CharField(max_length=256)

    def get_domain_name(self):
        name = urlparse(self.url).hostname
        if name.startswith('www.'):
            return name[len('www.'):]
        else:
            return name

    def set_upvoted(self, user, *, upvoted):
        if upvoted:
            PostUpvote.objects.get_or_create(post=self, user=user)
        else:
            self.upvotes.filter(user=user).delete()

    def to_dict(self, user):
        return {
            'title': self.title,
            'how_long_ago': self.how_long_ago(),
            'domain_name': self.get_domain_name(),
            'creator': self.creator.username,
            'upvoted': self.upvotes.filter(user=user).count() > 0,
            'comments_url': reverse('posts:comments', kwargs={'post_id': self.id}),
            'upvote_url': reverse('posts:set_upvoted_post', kwargs={'post_id': self.id}),
            'comments': [comment.to_dict(user) for comment in self.comments.filter(parent=None)]
        }


class PostUpvote(models.Model):
    post = models.ForeignKey(Post, related_name='upvotes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='post_upvotes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')


class Comment(models.Model, HowLongAgoMixin):
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('Comment', related_name='replies', on_delete=models.CASCADE, null=True, default=None)
    content = models.TextField(null=True)

    def set_upvoted(self, user, *, upvoted):
        if upvoted:
            CommentUpvote.objects.get_or_create(comment=self, user=user)
        else:
            self.upvotes.filter(user=user).delete()

    def to_dict(self, user):
        return {
            'content': self.content,
            'how_long_ago': self.how_long_ago(),
            'creator': self.creator.username,
            'upvoted': self.upvotes.filter(user=user).count() > 0,
            'comment_url': reverse('add_reply', kwargs={'comment_id': self.id}),
            'upvote_url': reverse('set_upvoted_comment', kwargs={'comment_id': self.id}),
            'replies': [
                reply.to_dict(user)
                for reply in self.replies.all()
            ],
        }


class CommentUpvote(models.Model):
    comment = models.ForeignKey(Comment, related_name='upvotes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_upvotes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')
