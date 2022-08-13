from django import views
from django.urls import path
from . import views

urlpatterns = [
    path("",views.starting_page.as_view(),name="starting-page"),
    path("posts",views.posts.as_view(),name="post-page"),
    path("posts/<slug>",views.post_detail.as_view(),name="post-detail-page"),
] 
