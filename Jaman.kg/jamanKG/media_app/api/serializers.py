from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    )
from media_app.models import Post

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [      # Comes from directly Model Post
            'title',
            #'slug',
            'content',
            'publish',
        ]

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'media_app-api:detail',
        lookup_field = 'slug'
        )
    delete_url = HyperlinkedIdentityField(
        view_name = 'media_app-api:delete',
        lookup_field = 'slug'
        )
    user = UserDetailSerializer(read_only = True)
    class Meta:
		model = Post
		fields = [		
            'url',
            'id',
            'user',
			'title',
			'content',
			'publish',
            'delete_url',
		]

class PostDetailSerializer(ModelSerializer):    # If i wanna see a different look than list view
    user = UserDetailSerializer(read_only = True)
    image = SerializerMethodField()
    markdown = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [      # Comes from directly Model Post
            'id',
            'title',
            'slug',
            'content',
            'markdown',
            'publish',
            'image', # Not works because your field is FileField vs ImageField
            'user',
            'comments',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_markdown(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj) #comment_qs; filter_by_instance() also defined by ourselves
        comments = CommentSerializer(c_qs, many = True).data
        return comments

"""
from posts.models import Post
from posts.api.serializers import PostDetailSerializer

data = {
    "title": "Bethany Benz",
    "content": "Top Model",
    "publish": "2016-2-12",   
    "slug": "bethany_benz", 
}

obj = Post.objects.get(id = 3)
new_item  = PostDetailSerializer(obj, data = data)	# First data is the keyword argument; Second is data above
if new_item.is_valid():
    new_item.save()
else:
    print new_item.errors
"""
