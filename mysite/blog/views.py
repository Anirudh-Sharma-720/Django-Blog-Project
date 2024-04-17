from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Post 
from django.views.generic import ListView
from .forms import CommentForm
from django.views import View

# Create your views here.

class StartingPageView(ListView) :
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView) :
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostDetail(View) :
    def is_stored_post(self,request, post_id) :
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None :
         is_saved_for_later = post_id in stored_posts
        else :
         is_saved_for_later = False
         
        return is_saved_for_later
       

    def get(self, request, slug) :
       post = Post.objects.get(slug=slug)
       
       context = {
           "post" : post,
           "post_tags": post.tags.all(),
           "comment_form" : CommentForm(),
           "comments" : post.comments.all().order_by("-id"),
           "saved_for_later" : self.is_stored_post(request, post.id)
       }
       return render(request, "blog/post-details-page.html", context)
    
    def post(sel, request, slug) :
         comment_form = CommentForm(request.POST)
         post = Post.objects.get(slug=slug)
         if comment_form.is_valid() :
              comment = comment_form.save(commit=False)
              comment.post = post
              comment.save()
              return HttpResponseRedirect(reverse("post-details-page", args = [slug]))
         
        
         context = {
           "post" : post,
           "post_tags": post.tags.all(),
           "comment_form" : comment_form,
           "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request, post.id)
            }
         return render(request, "blog/post-details-page.html", context)  
    


class ReadLaterView(View) :
    def get(self,request) :
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts)==0 :
            context["posts"] = []
            context["has_posts"] = False
        else : 
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True

        return render(request, "blog/stored-posts.html",context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None :
            stored_posts = []
        
        postid = int(request.POST["post_id"])
        if postid not in stored_posts :
              stored_posts.append(postid)
        else :
              stored_posts.remove(postid)
        
        request.session["stored_posts"]=stored_posts
        return HttpResponseRedirect("/")
