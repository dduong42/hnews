from datetime import datetime, timedelta
from unittest import mock

from django.test import TestCase

from .models import Post


class PostTestCase(TestCase):
    def test_how_long_0_seconds(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation
            self.assertEqual(post.how_long_ago(), '0 seconds ago')

    def test_how_long_1_second(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=1)
            self.assertEqual(post.how_long_ago(), '1 second ago')

    def test_how_long_multiple_seconds(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=42)
            self.assertEqual(post.how_long_ago(), '42 seconds ago')

    def test_how_long_1_minute(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=1)
            self.assertEqual(post.how_long_ago(), '1 minute ago')

    def test_how_long_multiple_minutes(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=42)
            self.assertEqual(post.how_long_ago(), '42 minutes ago')

    def test_how_long_1_hour(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=1)
            self.assertEqual(post.how_long_ago(), '1 hour ago')

    def test_how_long_multiple_hours(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=20)
            self.assertEqual(post.how_long_ago(), '20 hours ago')

    def test_how_long_1_day(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=1)
            self.assertEqual(post.how_long_ago(), '1 day ago')

    def test_how_long_multiple_days(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=20)
            self.assertEqual(post.how_long_ago(), '20 days ago')

    def test_how_long_multiple_days_limit(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(days=20, hours=23, minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '20 days ago')

    def test_how_long_multiple_hours_limit(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(hours=23, minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '23 hours ago')

    def test_how_long_multiple_minutes_limit(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(minutes=59, seconds=59)
            self.assertEqual(post.how_long_ago(), '59 minutes ago')

    def test_how_long_multiple_seconds_limit(self):
        creation = datetime(year=1966, month=6, day=6)

        post = Post(creation_date=creation)
        with mock.patch('hnews.posts.models.datetime') as dt:
            dt.now = mock.Mock()
            dt.now.return_value = creation + timedelta(seconds=59, milliseconds=999)
            self.assertEqual(post.how_long_ago(), '59 seconds ago')
