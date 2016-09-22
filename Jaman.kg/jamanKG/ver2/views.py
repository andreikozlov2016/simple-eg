# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.generic import View
# from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic.detail import DetailView
# from django.views.generic.list import ListView
# from django.core.urlresolvers import reverse
# from django.views.generic.edit import (
# 	CreateView,
# 	UpdateView,
# 	DeleteView,
# 	)


# from media_app.models import Post
# from media_app.forms import PostForm

# class LoginRequiredMixin(object):
# 	"""
# 	First way to do the login_required 
# 	in all needed classes.
# 	"""
# 	# @classmethod
# 	# def as_view(cls, **kwargs):
# 	# 	view = super(LoginRequiredMixin, cls).as_view(**kwargs)
# 	# 	return login_required(view)
# 	"""
# 	Second way to apply login_required
# 	to all classes. And more cleaner.
# 	"""
# 	@method_decorator(login_required)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

# class DashboardTemplateView(TemplateView):
# 	template_name = "index.html"

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
# 		context['title'] = "This is Class Based View"
# 		return context

# class MyView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
	
# 	def get(self, request, *args, **kwargs):
# 		context = self.get_context_data(**kwargs)
# 		context['title'] = "Other title"
# 		return self.render_to_response(context)
# 	"""
# 	Will work only for get() method
# 	What about others like post()?
# 	"""
# 	# @method_decorator(login_required)
# 	# def dispatch(self, request, *args, **kwargs):
# 	# 	return super(MyView, self).dispatch(request, *args, **kwargs)

# class PostDetail(DetailView):
# 	model = Post
# 	template_name = "post_detail.html"

# class PostListView(ListView):
# 	model = Post
# 	template_name = "post_list.html"

# 	def get_queryset(self, *args, **kwargs):
# 		qs = super(PostListView, self).get_queryset(*args, **kwargs).order_by("-id")
# 		# print qs
# 		# print qs.first()
# 		return qs

# """
# Creating the post
# """
# class PostCreateView(CreateView):
# 	model = Post
# 	template_name = "post_form.html"
# 	form_class = PostForm	
# 	#Definiing fields custom:	fields = ['title', 'content']		

# 	def form_valid(self, form):
# 		print form.instance
# 		form.instance.user = self.request.user
# 		return super(PostCreateView, self).form_valid(form)

# 	def get_success_url(self):
# 		return reverse('post_list_ver2')

# """
# Updating post
# """
# class PostUpdateView(UpdateView):
# 	form_class = PostForm
# 	template_name = "post_form.html"