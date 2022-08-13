from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .forms import CommentForm
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse  
from django.shortcuts import render
# Create your views here.


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts,
#     })

class starting_page(ListView):
    template_name="blog/index.html"
    model = Post
    context_object_name="posts"



# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts
#     })

class posts(ListView):
    template_name="blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"


# def post_detail(request, slug):
#     identified_post = Post.objects.get(slug=slug)     
#     return render(request, "blog/post-detail.html", {
#         "post":identified_post,
#         "post_tags":identified_post.tags.all()
#     })



class post_detail(View):
    # model = Post
    # template_name = "blog/post-detail.html"
    
    def get(self,request,slug):
 
        post=Post.objects.get(slug=slug)
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False )  
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))

        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form 
        }

        return render(request,"blog/post-detail.html",context)
    


class ReadLaterView(View):
    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id =int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        
        return HttpResponseRedirect("/")
