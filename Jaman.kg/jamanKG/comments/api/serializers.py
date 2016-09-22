from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
    )

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from accounts.api.serializers import UserDetailSerializer

User = get_user_model()

def create_comment_serializer(model_type = 'post', slug = None, parent_id = None, user = None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
            'id',        
            'content',
            'timestamp'
            ]

        #   Initializing the class with following args
        def __init__(self, *args, **kwargs):
            self.model_type = model_type # Variable assigned above
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id= parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        #   Process after user submits, check staff
        def validate(self, data):
            model_type = self.model_type  # Comes from __init__ func method above, not from create_comment_serializer
            model_qs = ContentType.objects.filter(model = model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not valid content type MAN")
            SomeModel = model_qs.first().model_class()  # TO be reb placeable by other Models 
            obj_qs = SomeModel.objects.filter(slug = self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not the slug for this model(content type) MAn")
            return data

            #   If you were doing this only for Post model; However we have to deal with GenericForeinKey 
            #   obj_qs = Post.objects.filter(slug = self.slug) 

        #   Collect the data above to create comment
        def create(self, validated_data):
            #   Args from comments/models/CommentManager/create_by_model_type()
            content = validated_data.get('content')
            if user:
                main_user = user  # main_user is submitting the staff
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type, 
                slug, 
                content,
                main_user, 
                parent_obj = parent_obj,
                )
            return comment
    return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [      # Comes from directly Model Comment
            'id',
            'content_type',
            'object_id',        
            'parent',
            'content',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name = 'comments-api:thread')

    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [ 
            'url',    
            'id',
            # 'content_type',
            # 'object_id',        
            # 'parent',
            'content',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(ModelSerializer):    
    user = UserDetailSerializer(read_only = True)   # comes from accounts/api/serializers
    class Meta:
        model = Comment
        fields = [     
            'user', 
            'id',       
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only = True)   # comes from accounts/api/serializers
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [  
            'user',   
            'id',
            # 'content_type',
            # 'object_id',        
            'content',
            'timestamp',
            'replies',
            'reply_count',
            'content_object_url',
        ]
        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'reply_count',
            'replies',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many = True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None


#   Don't need any longer, added read_only_fields above
# class CommentEditSerializer(ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = [    
#             'id',        
#             'content',
#             'timestamp',
#         ]
