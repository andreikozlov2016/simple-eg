from django.contrib import admin

# Register your models here.

from media_app.models import Post
from media_app.models import Actress


class PostModelAdmin(admin.ModelAdmin):
	list_display = ['title', 'time_added', 'updated']
	list_display_links = ['updated']
	list_filter = ['updated']
	list_editable = ['title']

	class Meta:
		model = Post

class ActressModelAdmin(admin.ModelAdmin):
	list_display = ['name', 'surname']



admin.site.register(Post, PostModelAdmin)
admin.site.register(Actress)