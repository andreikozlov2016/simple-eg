from django import forms
from pagedown.widgets import PagedownWidget
from media_app.models import Post
from taggit.managers import TaggableManager
from taggit.models import Tag



class PostForm(forms.ModelForm):
	content = forms.CharField(widget = PagedownWidget(show_preview = False))
	#publish = forms.DateField(widget = forms.SelectDateWidget)
	class Meta:
		model = Post
		fields = [		# Comes from directly Model Post
			'title',			
			'media_upload',
			'image',
			'content',	
			'tags',		
		]

    