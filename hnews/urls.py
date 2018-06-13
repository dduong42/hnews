from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from hnews.posts import views as posts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('hnews.posts.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('comments/<int:comment_id>/set_upvoted/', posts_views.set_upvoted_comment, name='set_upvoted_comment'),
    path('comments/<int:comment_id>/reply/', posts_views.add_reply, name='add_reply'),
]
