from django.contrib import admin

from .models import Post, Comment, Reaction, Activity, Following

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Following)
admin.site.register(Activity)
