from django.urls import include, path

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    # path("", views.PostList.as_view(), name="home"),
    path("", views.blog_list, name="home"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:pk>/", views.post_detail, name="post_detail"),
]
# {% url 'post_detail' post.slug  %}