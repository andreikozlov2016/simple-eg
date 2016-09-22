from __future__ import unicode_literals
from django.conf import settings
from django.db import models

from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe 
from markdown_deux import markdown
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time


from comments.models import Comment

from taggit.managers import TaggableManager

# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft = False).filter(publish__lte = timezone.now())

def upload_location(instance, filename):
	#  filebase, extension = filename.split('.')
	return '%s/%s' %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  related_name='post_edit')
	title = models.CharField(max_length = 40)
	slug = models.SlugField(unique = True)
	media_upload = models.FileField(upload_to = upload_location, 
		null = True, 
		blank = True
		) #upload_to = upload_location, 
	image = models.FileField(upload_to = upload_location, 
		null = True, 
		blank = True
		)
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	content = models.TextField()
	draft = models.BooleanField(default = False)
	publish = models.DateField(auto_now = True, auto_now_add = False)
	read_time = models.IntegerField(default = 0)	#models.TimeField(null = True, blank = True)
	time_added = models.DateTimeField(auto_now = False, auto_now_add = True)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	views = models.IntegerField(default = 0)

	objects = PostManager()

	tags = TaggableManager()

	def __unicode__(self):
			return self.title

	def __str__(self):
		return self.title 

	def get_absolute_url(self):
		return reverse('media_app:detail', kwargs = {'slug': self.slug})
		#return '/%s'%(self.id)

	def get_api_url(self):
		return reverse('media_app-api:detail', kwargs = {'slug': self.slug})

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown(content))

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type	


class Actress(models.Model):
	post = models.ForeignKey(Post)
	name = models.CharField(max_length = 20, blank = True)
	surname = models.CharField(max_length = 20, blank = True)

# class User(models.Model):
# 	username = models.CharField(max_length = 20)
# 	name = models.CharField(max_length = 20)
# 	surname = models.CharField(max_length = 20)
# 	joined = models.DateTimeField(auto_now_add = True)

# 	def __unicode__(self):
# 		return self.username

# 	def __str__(self):
# 		return self.username

def create_slug(instance, new_slug = None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug = slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = '%s-%s' %(slug, qs.first().id)
		return create_slug(instance, new_slug = new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	# slug = slugify(instance.title)
	# exists = Post.objects.filter(slug = slug).exists()
	# if exists:
	# 	slug = '%s-%s' %(slug, instance.id)
	# instance.slug = slug

	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender = Post)