try:
    from urllib import quote_plus #python 2
except:
    pass
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.



#from django.contrib import messages
from django.utils import timezone 
from django.db.models import Q


from django.contrib.contenttypes.models import ContentType


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from taggit.models import Tag

from django import forms
from django.http import HttpResponseForbidden
#from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

"""
Class based staff
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.contrib import messages 
from django.contrib.messages.views import SuccessMessageMixin
from comments.forms import CommentForm
from comments.models import Comment
from django.views.generic.edit import (
	CreateView,
	UpdateView,
	DeleteView,
	ModelFormMixin,
	)


from media_app.models import Post
from media_app.forms import PostForm
from comments.models import Comment, CommentManager
from comments.forms import CommentForm

class LoginRequiredMixin(object):
	"""
	First way to do the login_required 
	in all needed classes.
	"""
	# @classmethod
	# def as_view(cls, **kwargs):
	# 	view = super(LoginRequiredMixin, cls).as_view(**kwargs)
	# 	return login_required(view)
	"""
	Second way to apply login_required
	to all classes. And more cleaner.
	"""
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class DashboardTemplateView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, *args, **kwargs):
		context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
		context['title'] = "This is Class Based View"
		return context

class MyView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['title'] = "Other title"
		return self.render_to_response(context)
	"""
	Will work only for get() method
	What about others like post()?
	"""
	# @method_decorator(login_required)
	# def dispatch(self, request, *args, **kwargs):
	# 	return super(MyView, self).dispatch(request, *args, **kwargs)


"""
Tagging staff
"""
class TagMixin(object):
	def get_context_data(self, **kwargs):
	    context = super(TagMixin, self).get_context_data(**kwargs)
	    context['tags'] = Tag.objects.all().order_by('-id')
	    # context['most_popular'] = Post.objects.all()[0:8]
		# context['new_videos'] = Post.objects.all().order_by('-time_added')[0:8]
	    return context

class TagView(TagMixin, ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'posts'
	paginate_by = 8

	def get_queryset(self):		
		query = self.request.GET.get('q')
		if query:
			queryset_list = Post.objects.all().filter(
				Q(title__icontains = query) |
				Q(content__icontains = query) |
				Q(user__first_name__icontains = query) |
				Q(user__last_name__icontains = query) 
				).distinct()
			return queryset_list
		return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

# class CommentDetailView(FormMixin):
# 	model = Comment
# 	form = CommentForm
# 	queryset = Comment.objects.all()

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(CommentDetailView, self).get_context_data(*args, **kwargs)
# 		context['content_type'] = self.content_type
# 		context['object_id'] = self.object_id
# 		context['form'] = self.get_form()
# 		return context

# 	def post(self, request, *args, **kwargs):
# 		if not request.user.is_authenticated:
# 			return HttpResponseForbidden()
# 		self.object = self.get_object()
# 		form = self.get_form()
# 		if form.is_valid():
# 			return self.form_valid(form)
# 		else:
# 			return self.form_invalid(form)


# class CommentMixin(FormMixin):
# 	model = Comment
# 	class_form = CommentForm

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(CommentMixin, self).get_context_data(*args, **kwargs)
# 		context['form'] = self.get_form()
# 		context['comments'] = ''

# 	def post(self, request, *args, **kwargs):
# 		if not request.user.is_authenticated:
# 			return HttpResponseForbidden()
# 		self.object = self.get_object()
# 		form = self.get_form()
# 		if form.is_valid():
# 			return self.form_valid(form)
# 		else:
# 			return self.form_invalid(form)

"""
Post item(detail)
"""
class PostDetail(TagMixin, FormMixin, DetailView):
	model = Post
	template_name = "post_detail.html"
	form_class = CommentForm

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetail, self).get_context_data(*args, **kwargs)	
			
	 	context['form'] = self.get_form()
	 	print context

		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		print (self.object)
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
	    # Here, we would record the user's interest using the message
	    # passed in form.cleaned_data['message']
	    return super(PostDetail, self).form_valid(form)

	# def get_comments(self, obj):
	# 	content_type = obj.get_content_type
	# 	object_id = obj.id
	# 	c_qs = Comment.objects.filter_by_instance(obj)

	

	"""
	Extra things may be done in dispatch() method
	"""
	# def dispatch(self, request, *args, **kwargs):
	# 	messages.success(self.request, 'Mesajler')
	# 	return super(PostDetail, self).dispatch(request, *args, **kwargs)



# class PostDetail(FormMixin, DetailView):
#     model = Post
#     form_class = CommentForm
#     template_name = 'post_detail.html'

#     # def get_success_url(self):
#     #     return reverse('media_app:detail', kwargs={'slug': self.object.slug})

#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         # Here, we would record the user's interest using the message
#         # passed in form.cleaned_data['message']
#         return super(PostDetail, self).form_valid(form)




"""
List of posts
"""
class PostListView(TagMixin, ListView):
	model = Post
	template_name = "index.html"
	paginate_by = 8

	def get_queryset(self):
		# qs = super(PostListView, self).get_queryset(*args, **kwargs).order_by("-id")
		# # print qs
		# # print qs.first()
		# return qs
		queryset_list = Post.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains = query) |
				Q(content__icontains = query) |
				Q(user__first_name__icontains = query) |
				Q(user__last_name__icontains = query) 
				).distinct()
		return queryset_list


"""
Creating the post
"""
class PostCreateView(TagMixin, SuccessMessageMixin, CreateView):
	model = Post
	template_name = "post_form.html"
	form_class = PostForm	
	success_message = "%(title)s has been created"
	#Definiing fields custom:	fields = ['title', 'content']		

	def form_valid(self, form):
		# print form.instance
		form.instance.user = self.request.user
		valid_form = super(PostCreateView, self).form_valid(form)
		#Custom message rendering: messages.success(self.request, "Some message"), but mixin is better.


		return valid_form

	def get_success_url(self):
		return reverse('media_app:detail', kwargs={'slug': self.object.slug})


"""
Updating post
"""
class PostUpdateView(TagMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = "post_form.html"


"""
Deleting post
"""
class PostDeleteView(TagMixin, DeleteView):
	model = Post
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse('media_app:index')











# class IndexView(TagMixin):	
# 	paginate_by = 10
	
# 	def get_queryset(self):	
# 		queryset_list = Post.objects.all()

# 		### Serching items 
# 		query = self.request.GET.get('q')
# 		if query:
# 			queryset_list = queryset_list.filter(
# 				Q(title__icontains = query) |
# 				Q(content__icontains = query) |
# 				Q(user__first_name__icontains = query) |
# 				Q(user__last_name__icontains = query) 
# 				).distinct()
# 		return queryset_list	

# def post_create(request):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404

# 	# if not request.user.is_authenticated():
# 	# 	raise Http404

# 	form = PostForm(request.POST or None, request.FILES or None)
# 	if form.is_valid():
# 		instance = form.save(commit = False)
# 		instance.user = request.user
# 		instance.save()
# 		#messages.success(request, 'Successfully created')
# 		form.save_m2m()	# Saving the tag
# 		return HttpResponseRedirect(instance.get_absolute_url())

# 	context = {
# 		'form': form,
# 	}
# 	return render(request, 'post_form.html', context)

# def post_detail(request, slug = None):

# 	#instance = Post.objects.get(id = 3)


# 	instance = get_object_or_404(Post, slug = slug)

# 	if instance.draft or instance.publish > timezone.now().date() or instance.draft:
# 		if not request.user.is_staff or not request.user.is_superuser:
# 			raise Http404

# 	#share_string = quote_plus(instance.content)

# 	initial_data = {
# 		'content_type': instance.get_content_type,
# 		'object_id': instance.id, 
# 	}

# 	form = CommentForm(request.POST or None, initial = initial_data)
# 	if form.is_valid() and request.user.is_authenticated():
# 		c_type = form.cleaned_data.get("content_type")
# 		content_type = ContentType.objects.get(model = c_type)
# 		obj_id = form.cleaned_data.get("object_id")
# 		content_data = form.cleaned_data.get("content")
# 		parent_obj = None
# 		try:
# 			parent_id = int(request.POST.get("parent_id"))
# 		except:
# 			parent_id = None

# 		if parent_id:
# 			parent_qs = Comment.objects.filter(id = parent_id)
# 			if parent_qs.exists() and parent_qs.count() == 1:
# 				parent_obj = parent_qs.first()
# 		new_comment, created = Comment.objects.get_or_create(
# 			user = request.user,
# 			content_type =  content_type,
# 			object_id = obj_id,
# 			content = content_data,
# 			parent = parent_obj,
# 			)

# 		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

# 	comments = instance.comments
# 	context = {
# 		'title': instance.title,
# 		'instance': instance,
# 		#'share_string': share_string,
# 		'comments': comments,
# 		'form': form,
# 	}

# 	return render(request, 'post_detail.html', context)

# def post_list(request):

# 	queryset_list = Post.objects.active().order_by('-time_added')
# 	#if request.user.is_staff or request.user.superuser:
# 	if request.user or request.user.superuser:
# 		queryset_list =  Post.objects.all()

# 	###	Searching items
# 	query = request.GET.get('q')
# 	if query:
# 		queryset_list = queryset_list.filter(
# 			Q(title__icontains = query) |
# 			Q(content__icontains = query) |
# 			Q(user__first_name__icontains = query) |
# 			Q(user__last_name__icontains = query) 
# 			).distinct()

# 	### Paginating
# 	paginator = Paginator(queryset_list, 20) # Show 2 contacts per page
# 	page_request_var = 'page' 	# What will appear in domain: ?page=x
# 	page = request.GET.get(page_request_var)
# 	today = timezone.now().date()
# 	try:
# 		queryset = paginator.page(page)
# 	except PageNotAnInteger:
# 		# If page is not an integer, deliver first page.
# 		queryset = paginator.page(1)
# 	except EmptyPage:
# 		# If page is out of range (e.g. 9999), deliver last page of results.
# 		queryset = paginator.page(paginator.num_pages)


# 	context = {
# 		'object_list': queryset,
# 		'title': 'List',
# 		'page_request_var': page_request_var,
# 		'today': today,
# 	}

# 	return render(request, 'post_list.html', context)



	# if request.user.is_authenticated():
	# 	context = {
	# 		'title': 'My user list'
	# 	}
	# else:
	# 	context = {
	# 		'title': 'List'
	# 	}


# def post_update(request, slug = None):

# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404

# 	instance = get_object_or_404(Post, slug = slug)

# 	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
# 	if form.is_valid():
# 		instance = form.save(commit = False)
# 		instance.save()
# 		messages.success(request, 'Changes were applied')
# 		return HttpResponseRedirect(instance.get_absolute_url())

# 	context = {
# 		'title': instance.title,
# 		'instance': instance,
# 		'form': form,
# 	}

# 	return render(request, 'post_form.html', context)


	

# def post_delete(request, slug = None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Post, slug = slug)
# 	instance.delete()
# 	messages.success(request, 'Changes were applied, post were deleted')
# 	return redirect('media_app: list')


# def popular(request, slug = None):
# 	queryset_list = Post.objects.active().order_by('-time_added')
# 	if request.user.is_staff or request.user.superuser:
# 		queryset_list =  Post.objects.all()

# 	query = request.GET.get('q')
# 	if query:
# 		queryset_list = queryset_list.filter(
# 			Q(title__icontains = query) |
# 			Q(content__icontains = query) |
# 			Q(user__first_name__icontains = query) |
# 			Q(user__last_name__icontains = query) 
# 			).distinct()
# 	paginator = Paginator(queryset_list, 4) # Show 24 contacts per page
# 	page_request_var = 'page'
# 	page = request.GET.get(page_request_var)
# 	today = timezone.now().date()
# 	try:
# 		queryset = paginator.page(page)
# 	except PageNotAnInteger:
# 		# If page is not an integer, deliver first page.
# 		queryset = paginator.page(1)
# 	except EmptyPage:
# 		# If page is out of range (e.g. 9999), deliver last page of results.
# 		queryset = paginator.page(paginator.num_pages)


# 	context = {
# 		'object_list': queryset,
# 		'title': 'List',
# 		'page_request_var': page_request_var,
# 		'today': today,
# 	}

# 	return render(request, 'popular.html', context)
	
# def palette(request, slug = None):
# 	context  ={
	
# 	}
# 	return render(request, 'palette.html', context)

# def index(request, slug = None):
# 	# queryset_list = Post.objects.active().order_by('-time_added')
# 	# if request.user.is_staff or request.user.superuser:
# 	# 	queryset_list =  Post.objects.all()[0:8]

# 	# query = request.GET.get('q')
# 	# if query:
# 	# 	queryset_list = queryset_list.filter(
# 	# 		Q(title__icontains = query) |
# 	# 		Q(content__icontains = query) |
# 	# 		Q(user__first_name__icontains = query) |
# 	# 		Q(user__last_name__icontains = query) 
# 	# 		).distinct()

# 	# queryset = queryset_list
	

# 	# context = {
# 	# 	'object_list': queryset,
# 	# 	'title': 'List',
		
# 	# }

# 	# return render(request, 'index.html', context)


# 	most_popular = Post.objects.all()[0:8]
# 	new_videos = Post.objects.all().order_by('-time_added')[0:8]
	

# 	context = {
# 		"most_popular": most_popular,
# 		"new_videos": new_videos,
		
# 	}

# 	return render(request, 'index.html', context)

# def base(request, slug = None):
# 	context  ={
	
# 	}
# 	return render(request, 'base.html', context)


# def index0(request, slug = None):
# 	context  ={
	
# 	}
# 	return render(request, 'index0.html', context)



# def new_videos(request, slug = None):
# 	queryset_list = Post.objects.active().order_by('time_added')
# 	if request.user.is_staff or request.user.superuser:
# 		queryset_list =  Post.objects.all()

# 	query = request.GET.get('q')
# 	if query:
# 		queryset_list = queryset_list.filter(
# 			Q(title__icontains = query) |
# 			Q(content__icontains = query) |
# 			Q(user__first_name__icontains = query) |
# 			Q(user__last_name__icontains = query) 
# 			).distinct()
# 	paginator = Paginator(queryset_list, 24) # Show 2 contacts per page
# 	page_request_var = 'page'
# 	page = request.GET.get(page_request_var)
# 	today = timezone.now().date()
# 	try:
# 		queryset = paginator.page(page)
# 	except PageNotAnInteger:
# 		# If page is not an integer, deliver first page.
# 		queryset = paginator.page(1)
# 	except EmptyPage:
# 		# If page is out of range (e.g. 9999), deliver last page of results.
# 		queryset = paginator.page(paginator.num_pages)


# 	context = {
# 		'object_list': queryset,
# 		'title': 'List',
# 		'page_request_var': page_request_var,
# 		'today': today,
# 	}

# 	return render(request, 'new_videos.html', context)

# def video_test(request):
# 	return render(request, 'video.html')

# def video_test(request):
#     posts_list = Post.objects.all().order_by('time_added')

#     paginator = Paginator(posts_list, 2)

#     try:
#         page = int(request.GET.get('page', '1'))
#     except:
#         page = 1

#     try:
#         posts = paginator.page(page)
#     except(EmptyPage, InvalidPage):
#         posts = paginator.page(paginator.num_pages)

    
#     return render(request, 'video.html', {'posts': posts, 'posts_list': posts_list})


		
	
"""
"""
# class PostListAPIView(ListAPIView):
# 	serializer_class = PostListSerializer
# 	filter_backends = [SearchFilter, OrderingFilter]
# 	search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
# 	pagination_class = PostPageNumberPagination #PageNumberPagination
# 	permission_classes = [AllowAny]

# 	def get_queryset(self, *args, **kwargs):	
# 		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
# 		queryset_list = Post.objects.all()	

# 		### Serching items 
# 		query = self.request.GET.get('q')
# 		if query:
# 			queryset_list = queryset_list.filter(
# 				Q(title__icontains = query) |
# 				Q(content__icontains = query) |
# 				Q(user__first_name__icontains = query) |
# 				Q(user__last_name__icontains = query) 
# 				).distinct()
# 		return queryset_list


# class PostListSerializer(ModelSerializer):
#     url = HyperlinkedIdentityField(
#         view_name = 'media_app-api:detail',
#         lookup_field = 'slug'
#         )
#     delete_url = HyperlinkedIdentityField(
#         view_name = 'media_app-api:delete',
#         lookup_field = 'slug'
#         )
#     user = UserDetailSerializer(read_only = True)
#     class Meta:
# 		model = Post
# 		fields = [		
#             'url',
#             'id',
#             'user',
# 			'title',
# 			'content',
# 			'publish',
#             'delete_url',
# 		]


# def index(request, slug = None):
# 	# queryset_list = Post.objects.active().order_by('-time_added')
# 	# if request.user.is_staff or request.user.superuser:
# 	# 	queryset_list =  Post.objects.all()[0:8]

# 	# query = request.GET.get('q')
# 	# if query:
# 	# 	queryset_list = queryset_list.filter(
# 	# 		Q(title__icontains = query) |
# 	# 		Q(content__icontains = query) |
# 	# 		Q(user__first_name__icontains = query) |
# 	# 		Q(user__last_name__icontains = query) 
# 	# 		).distinct()

# 	# queryset = queryset_list
	

# 	# context = {
# 	# 	'object_list': queryset,
# 	# 	'title': 'List',
		
# 	# }

# 	# return render(request, 'index.html', context)


# 	most_popular = Post.objects.all()[0:8]
# 	new_videos = Post.objects.all().order_by('-time_added')[0:8]
	

# 	context = {
# 		"most_popular": most_popular,
# 		"new_videos": new_videos,
		
# 	}

# 	return render(request, 'index.html', context)



# class PostDetailAPIView(RetrieveAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = "slug"	# By deafult is pk. IF not set your slug will be ignored, 
# 							# and goes directly to item without slug.
# 	permission_classes = [AllowAny]

# def post_detail(request, slug = None):

# 	#instance = Post.objects.get(id = 3)


# 	instance = get_object_or_404(Post, slug = slug)

# 	if instance.draft or instance.publish > timezone.now().date() or instance.draft:
# 		if not request.user.is_staff or not request.user.is_superuser:
# 			raise Http404

# 	#share_string = quote_plus(instance.content)

# 	initial_data = {
# 		'content_type': instance.get_content_type,
# 		'object_id': instance.id, 
# 	}

# 	form = CommentForm(request.POST or None, initial = initial_data)
# 	if form.is_valid() and request.user.is_authenticated():
# 		c_type = form.cleaned_data.get("content_type")
# 		content_type = ContentType.objects.get(model = c_type)
# 		obj_id = form.cleaned_data.get("object_id")
# 		content_data = form.cleaned_data.get("content")
# 		parent_obj = None
# 		try:
# 			parent_id = int(request.POST.get("parent_id"))
# 		except:
# 			parent_id = None

# 		if parent_id:
# 			parent_qs = Comment.objects.filter(id = parent_id)
# 			if parent_qs.exists() and parent_qs.count() == 1:
# 				parent_obj = parent_qs.first()
# 		new_comment, created = Comment.objects.get_or_create(
# 			user = request.user,
# 			content_type =  content_type,
# 			object_id = obj_id,
# 			content = content_data,
# 			parent = parent_obj,
# 			)

# 		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

# 	comments = instance.comments
# 	context = {
# 		'title': instance.title,
# 		'instance': instance,
# 		#'share_string': share_string,
# 		'comments': comments,
# 		'form': form,
# 	}

# 	return render(request, 'post_detail.html', context)

# class CommentForm(forms.form)

# class PostDetailView(FormMixin, DetailView):
#     model = Post
#     form_class = CommentForm
#     template_name = 'post_detail.html'
#     comments = Comment.objects.all()


#     def get_success_url(self):
#         return reverse('media_app:detail', kwargs={'slug': self.object.slug})

#     def get_context_data(self, **kwargs):
#         context = super(PostDetailView, self).get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         # Here, we would record the user's interest using the message
#         # passed in form.cleaned_data['message']
#         return super(PostDetailView, self).form_valid(form)


       