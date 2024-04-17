from django.contrib import admin

# Register your models here.
from .models import Author,Tag,Post, Comment



class PostAdmin(admin.ModelAdmin):
    list_filter = ("author","date","tags",)
    list_display = ("title","date","author")
    prepopulated_fields = {"slug" : ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name","text", "post")

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)

