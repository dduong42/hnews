import json
from datetime import datetime, timedelta, timezone
from unittest import mock

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase

from .models import Comment, Post


class PostTestCase(TestCase):
    def test_how_long_0_seconds(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation
            self.assertEqual(post.how_long_ago(), '0 seconds ago')

    def test_how_long_1_second(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=1)
            self.assertEqual(post.how_long_ago(), '1 second ago')

    def test_how_long_multiple_seconds(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=42)
            self.assertEqual(post.how_long_ago(), '42 seconds ago')

    def test_how_long_1_minute(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=1)
            self.assertEqual(post.how_long_ago(), '1 minute ago')

    def test_how_long_multiple_minutes(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=42)
            self.assertEqual(post.how_long_ago(), '42 minutes ago')

    def test_how_long_1_hour(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=1)
            self.assertEqual(post.how_long_ago(), '1 hour ago')

    def test_how_long_multiple_hours(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=20)
            self.assertEqual(post.how_long_ago(), '20 hours ago')

    def test_how_long_1_day(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=1)
            self.assertEqual(post.how_long_ago(), '1 day ago')

    def test_how_long_multiple_days(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=20)
            self.assertEqual(post.how_long_ago(), '20 days ago')

    def test_how_long_multiple_days_limit(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=20, hours=23, minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '20 days ago')

    def test_how_long_multiple_hours_limit(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=23, minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '23 hours ago')

    def test_how_long_multiple_minutes_limit(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '59 minutes ago')

    def test_how_long_multiple_seconds_limit(self):
        creation = datetime(year=1966, month=6, day=6, tzinfo=timezone.utc)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.timezone') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=59, milliseconds=999)
            self.assertEqual(post.how_long_ago(), '59 seconds ago')

    def test_domain_name(self):
        post = Post(url='https://techcrunch.com/2018/06/05/washington-sues-facebook-and-google-over-failure-to-disclose-political-ad-spending/')
        self.assertEqual(post.get_domain_name(), 'techcrunch.com')

    def test_domain_name_with_subdomain(self):
        post = Post(url='https://blog.mozilla.org/nnethercote/2018/06/05/how-to-speed-up-the-rust-compiler-some-more-in-2018/')
        self.assertEqual(post.get_domain_name(), 'blog.mozilla.org')

    def test_domain_name_with_www(self):
        post = Post(url='https://www.livescience.com/61627-ancient-virus-brain.html')
        self.assertEqual(post.get_domain_name(), 'livescience.com')

    def test_set_upvoted_true(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        post.set_upvoted(user, upvoted=True)
        self.assertEqual(1, post.upvotes.filter(id=user.id).count())

    def test_set_upvoted_false(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        post.set_upvoted(user, upvoted=True)
        post.set_upvoted(user, upvoted=False)
        self.assertEqual(0, post.upvotes.filter(id=user.id).count())


class CommentTestCase(TestCase):
    def test_set_upvoted_true(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        comment = Comment.objects.create(creator=user, content='Cool', post=post)
        comment.set_upvoted(user, upvoted=True)
        self.assertEqual(1, comment.upvotes.filter(id=user.id).count())

    def test_set_upvoted_false(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        comment = Comment.objects.create(creator=user, content='Cool', post=post)
        comment.set_upvoted(user, upvoted=True)
        comment.set_upvoted(user, upvoted=False)
        self.assertEqual(0, comment.upvotes.filter(id=user.id).count())


class SetUpvotedTestCase(TestCase):
    def test_set_upvoted_true_creates_post_upvote(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        client = Client()

        client.login(username='jean', password='hey')
        uri = reverse('posts:set_upvoted_post', kwargs={'post_id': post.id})
        client.post(uri, json.dumps({'upvoted': True}), content_type='application/json')
        self.assertEqual(1, post.upvotes.filter(id=user.id).count())

    def test_set_upvoted_true_returns_204(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        client = Client()

        client.login(username='jean', password='hey')
        uri = reverse('posts:set_upvoted_post', kwargs={'post_id': post.id})
        response = client.post(uri, json.dumps({'upvoted': True}), content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_set_upvoted_needs_authentication(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        client = Client()

        uri = reverse('posts:set_upvoted_post', kwargs={'post_id': post.id})
        response = client.post(uri, json.dumps({'upvoted': True}), content_type='application/json')
        # It should redirect to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/accounts/login/?next={uri}')

    def test_set_upvoted_false_removes_post_upvote(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        client = Client()

        client.login(username='jean', password='hey')
        uri = reverse('posts:set_upvoted_post', kwargs={'post_id': post.id})
        client.post(uri, json.dumps({'upvoted': True}), content_type='application/json')
        client.post(uri, json.dumps({'upvoted': False}), content_type='application/json')
        self.assertEqual(0, post.upvotes.filter(id=user.id).count())

    def test_set_upvoted_false_returns_204(self):
        user = User.objects.create_user(username='jean', email='jean@example.com', password='hey')
        post = Post.objects.create(url='https://google.com', title='Google', creator=user)
        client = Client()

        client.login(username='jean', password='hey')
        uri = reverse('posts:set_upvoted_post', kwargs={'post_id': post.id})
        response = client.post(uri, json.dumps({'upvoted': False}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
