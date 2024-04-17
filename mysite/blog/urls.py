from django.urls import path
from . import views

# declaring url Pattern for mapping views
urlpatterns = [
    path("",views.StartingPageView.as_view(),name="starting-page"),
    path("posts",views.AllPostsView.as_view(),name="posts-page"),
    path("posts/<slug:slug>",views.SinglePostDetail.as_view(),name="post-details-page"),
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
]
