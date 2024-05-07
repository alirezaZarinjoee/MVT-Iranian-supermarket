from django.contrib import admin
from . models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['product','commenting_user','comment_text','is_active','register_date',]
    list_editable=['is_active']