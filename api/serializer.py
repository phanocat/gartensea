from rest_framework import serializers
from .models import Post, Image, Attachment, Comment, Customization, Tag, Article, ArticleComment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'post']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'text', 'type', 'post']

class PostSupplementsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['images', 'attachments']

class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'comments_count']

class PostTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text']

class FullPostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'images', 'attachments']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'is_active', 'is_superuser']

class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'is_superuser']

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class CommentSerializer(serializers.ModelSerializer):
    author = FullUserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at', 'post']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

    def validate_username(self, value):
        exist_contact = User.objects.filter(username=value)
        if exist_contact:
            username = get_object_or_404(User, username=value)
            if username != '':
                raise serializers.ValidationError('Указанный логин уже используется.')
        return value

class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name']

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class FullCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'type', 'content', 'file']

class ContentCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'type', 'content']
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class CreateArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at', 'text', 'description', 'tags', 'cover']
        
class ArticleCommentSerializer(serializers.ModelSerializer):
    author = FullUserSerializer()

    class Meta:
        model = ArticleComment
        fields = ['id', 'text', 'author', 'created_at']

class FullArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source='article_comments.count',
        read_only=True
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at', 'text', 'description', 'tags', 'cover', 'comments_count']
        
class ArticleCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id', 'text', 'author', 'created_at', 'article']
        
