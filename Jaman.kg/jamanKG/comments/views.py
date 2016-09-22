from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

from django.contrib.auth.decorators import login_required

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
from django.views.generic.edit import (
	CreateView,
	UpdateView,
	DeleteView,
	ModelFormMixin,
	)


from media_app.models import Post
from media_app.forms import PostForm


# Create your views here.

@login_required		#(login_url = "/login/") # You may chnage in settings to -> LOGIN_URL = '/login/'
def comment_delete(request, id):
	#obj = get_object_or_404(Comment, id = id)

	# Check if comment exists
	try:
		obj = Comment.objects.get(id = id)
	except:
		raise Http404
	# Check that comments owner is this user
	if obj.user != request.user:
		# messages.success(request, "You don't have a permission to view this.")
		# raise Http404
		response = HttpResponse("You don't have a permission to do this.")
		response.status_code = 403
		return response
		#return render(request, "confirm_delete.html", context, status_code = 403)

	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "This comment was deleted.")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object": obj
	}
	return render(request, "confirm_delete.html", context)


def comment_thread(request, id):
	#obj = get_object_or_404(Comment, id = id)
	try:
		obj = Comment.objects.get(id = id)
	except:
		raise Http404
	if not obj.is_parent:
		obj = obj.parent
	content_object = obj.content_object
	content_id = obj.content_object.id
	initial_data = {
		'content_type': obj.content_type,
		'object_id': obj.object_id, 
	}

	form = CommentForm(request.POST or None, initial = initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model = c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id = parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()
		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type =  content_type,
			object_id = obj_id,
			content = content_data,
			parent = parent_obj,
			)

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"comment": obj,
		'form': form,
	}
	return render(request, "comment_thread.html", context)

"""
Creating the comment
"""
class CommentCreateView(SuccessMessageMixin, CreateView):
	model = Comment
	template_name = "post_form.html"
	#form_class = CommentForm	
	#uccess_message = "%(title)s has been created"
	#Definiing fields custom:	fields = ['title', 'content']	

	# def get_context_data(self, *args, **kwargs):
	# 	model_type = self.request.GET.get('type')
	# 	slug = self.get.request.GET.get('slug')
	# 	parent_id = self.get.request.GET.get('parent_id', None)

	# def form_valid(self, form):
	# 	# print form.instance
	# 	form.instance.user = self.request.user
	# 	valid_form = super(CommentCreateView, self).form_valid(form)
	# 	#Custom message rendering: messages.success(self.request, "Some message"), but mixin is better.


	# 	return valid_form

	# def get_success_url(self):
	# 	return reverse('media_app:detail', kwargs={'slug': self.object.slug})


class CommentDetailView(DetailView):            #FormMixin, 
	queryset = Comment.objects.all()
	for i in queryset:
		print i.pk
	print object

	
	# model = Comment
	template_name = "parent_comment.html"
	context_object_name = 'comment'
	# form_class = CommentForm

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(CommentDetailView, self).get_context_data(*args, **kwargs)
	# 	context['form'] = self.get_form()
	# 	return context

	# def post(self, request, *args, **kwargs):
	# 	if not request.user.is_authenticated:
	# 		return HttpResponseForbidden()
	# 	self.object = self.get_object()
	# 	form = self.get_form()
	# 	if form.is_valid():
	# 		return self.form_valid(form)
	# 	else:
	# 		return self.form_invalid(form)



class CommentListView(ListView):
    # model = Comment
    template_name = "comment_thread.html"
    # form = CommentForm

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Comment.objects.all())
    #     return super(CommentListView, self).get(request, *args, **kwargs)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(CommentListView, self).get_context_data(*args, **kwargs)
    #     context['id'] = self.id
    #     return context

    def get_queryset(self):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
            Q(content__icontains = query) |
            Q(user__first_name__icontains = query) |
            Q(user__last_name__icontains = query) 
            ).distinct()
        return queryset_list

