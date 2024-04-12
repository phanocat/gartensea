from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth import authenticate, login, logout
from .models import Post, Image, Attachment, Comment, Customization
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .serializer import PostSerializer, ImageSerializer, PostSupplementsSerializer, FullPostSerializer, \
    PostTextSerializer, AttachmentSerializer, CommentSerializer, CommentCreateSerializer, \
    FullUserSerializer, UserRegistrationSerializer, UserProfileRegistrationSerializer,\
    FullCustomizationSerializer, ContentCustomizationSerializer, \
    UserListSerializer

class PostView(viewsets.ViewSet):
    def retrieve(self, request, post_id):
        queryset = Post.objects.all()
        item = get_object_or_404(queryset, pk=post_id)
        serializer = PostSerializer(item)
        return Response(serializer.data)
        
    def count(self, request):
        posts = Post.objects.all().filter(is_new_post=False)
        postsCount = posts.count()
        return Response(postsCount)

    def list(self, request, loadedCount, limit):
        queryset = Post.objects.all().filter(is_new_post=False).order_by('-created_at')
        posts = queryset[loadedCount:loadedCount+limit]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post_supplements_list(self, request, post_id):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=post_id)
        serializer = PostSupplementsSerializer(post)
        return Response(serializer.data)

    def get_new_post(self, request):
        queryset = Post.objects
        post, created = queryset.get_or_create(is_new_post=True)
        serializer = FullPostSerializer(post)
        return Response(serializer.data)

    def set_text(self, request, post_id):
        data = request.data
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=post_id)
        serializer = PostTextSerializer(post, data=data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def create(self, request):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, is_new_post=True)
        post.is_new_post = False
        post.created_at = datetime.datetime.now()
        post.save()
        serializer = FullPostSerializer(post)
        return Response(serializer.data)

    def delete(self, request):
        id = request.data.get('post_id')
        post = get_object_or_404(Post.objects, id=id)
        images = Image.objects.all().filter(post=post)
        for image in images:
            image.file.delete(save=True)
        post.delete()
        return Response(True)

class CommentView(viewsets.ViewSet):
    def list(self, request, post_id, loadedItemsCount):
        comments = Comment.objects.filter(post__id=post_id)[loadedItemsCount:loadedItemsCount+30]
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def count(self, request, post_id):
        items = Comment.objects.all().filter(post__id=post_id)
        count = items.count()
        return Response(count)

    def create(self, request):
        data = request.data
        _mutable = data._mutable
        data._mutable = True
        data['author'] = request.user.pk
        data._mutable = _mutable
        serializer = CommentCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        new_comment = serializer.save()
        show_data_serializer = CommentSerializer(new_comment)
        return Response(show_data_serializer.data)

class ImageView(viewsets.ViewSet):
    def add_image(self, request):
        data = request.data
        serializer = ImageSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        id = request.data.get('image_id')
        image = get_object_or_404(Image.objects, id=id)
        image.file.delete(save=True)
        image.delete()
        return Response(True)

class AttachmentView(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        serializer = AttachmentSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        id = request.data.get('attachment_id')
        attachment = get_object_or_404(Attachment.objects, id=id)
        attachment.delete()
        return Response(True)

class UserView(viewsets.ViewSet):
    def count(self, request):
        users = User.objects.all()
        count = users.count()
        return Response(count)

    def search_list(self, request):
        data = request.data
        search_str = data.get('searchStr')
        loaded_items_count = int(data.get('loadedItemsCount'))
        queryset = User.objects.all().filter(Q(first_name__icontains=search_str))
        queryset = queryset.order_by('-pk')
        users = queryset[loaded_items_count:loaded_items_count+30]
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def user_list(self, request, total_count):
        queryset = User.objects.all().order_by('-pk')
        users = queryset[total_count:total_count+30]
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=request.user.pk)
        serializer = FullUserSerializer(user)
        return Response(serializer.data)

    def login_or_registration(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        operation = data.get('operation')
        if operation == 'registration':
            serializer = UserRegistrationSerializer(data=data)
            if not serializer.is_valid():
                return Response(status=400, data=serializer.errors)
            user = serializer.save()
            user.is_active = True
            user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response(status=404, data={"error": "Эти данные не позволяют авторизироваться."})
        return Response(True)

    def profile_create(self, request):
        data = request.data
        queryset = User.objects.all()
        user = request.user
        user = get_object_or_404(queryset, pk=user.pk)
        serializer = UserProfileRegistrationSerializer(user, data=data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def change_name(self, request):
        name = request.data.get('name')
        user = request.user
        user.first_name = name
        user.save()
        return Response(True)

    def change_email(self, request):
        email = request.data.get('email')
        user = request.user
        user.email = email
        user.save()
        return Response(True)

    def logout(self, request):
        logout(request)
        return Response(True)

    def block(self, request):
        id = request.data.get('user_id')
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response({'result': True, 'is_active': user.is_active})

class CustomizationView(viewsets.ViewSet):
    def profile_info(self, request):
        queryset = Customization.objects.all()
        avatar, created = queryset.get_or_create(type='avatar')
        avatar_serializer = FullCustomizationSerializer(avatar)
        name, created = queryset.get_or_create(type='name')
        name_serializer = FullCustomizationSerializer(name)
        email, created = queryset.get_or_create(type='email')
        email_serializer = FullCustomizationSerializer(email)
        city, created = queryset.get_or_create(type='city')
        city_serializer = FullCustomizationSerializer(city)
        status, created = queryset.get_or_create(type='status')
        status_serializer = FullCustomizationSerializer(status)
        data = {
            'avatar': avatar_serializer.data['file'],
            'name': name_serializer.data['content'],
            'email': email_serializer.data['content'],
            'city': city_serializer.data['content'],
            'status': status_serializer.data['content'],
        }
        return Response(data)

    def profile_about(self, request):
        queryset = Customization.objects.all()
        about, created = queryset.get_or_create(type='about')
        about_serializer = FullCustomizationSerializer(about)
        books, created = queryset.get_or_create(type='books')
        books_serializer = FullCustomizationSerializer(books)
        games, created = queryset.get_or_create(type='games')
        games_serializer = FullCustomizationSerializer(games)
        movies, created = queryset.get_or_create(type='movies')
        movies_serializer = FullCustomizationSerializer(movies)
        music, created = queryset.get_or_create(type='music')
        music_serializer = FullCustomizationSerializer(music)
        job, created = queryset.get_or_create(type='job')
        job_serializer = FullCustomizationSerializer(job)
        hobby, created = queryset.get_or_create(type='hobby')
        hobby_serializer = FullCustomizationSerializer(hobby)
        quotes, created = queryset.get_or_create(type='quotes')
        quotes_serializer = FullCustomizationSerializer(quotes)
        words, created = queryset.get_or_create(type='words')
        words_serializer = FullCustomizationSerializer(words)
        data = {
            'about': about_serializer.data['content'],
            'books': books_serializer.data['content'],
            'games': games_serializer.data['content'],
            'movies': movies_serializer.data['content'],
            'music': music_serializer.data['content'],
            'job': job_serializer.data['content'],
            'hobby': hobby_serializer.data['content'],
            'quotes': quotes_serializer.data['content'],
            'words': words_serializer.data['content'],
        }
        return Response(data)

    def profile_contacts(self, request):
        queryset = Customization.objects.all()
        item, created = queryset.get_or_create(type='contacts')
        serializer = ContentCustomizationSerializer(item)
        return Response(serializer.data['content'])

    def privacy_settings_data(self, request):
        try:
            item = Customization.objects.all().get(type='needToEnter')
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            item = Customization.objects.filter(type='needToEnter').order_by('id').first()
            Customization.objects.all().filter(type='needToEnter').exclude(pk=item.pk).delete()
        serializer = ContentCustomizationSerializer(item)
        return Response(serializer.data['content'])

    def styles(self, request):
        queryset = Customization.objects.all()
        background, created = queryset.get_or_create(type='background')
        background_serializer = FullCustomizationSerializer(background)
        color, created = queryset.get_or_create(type='color')
        color_serializer = ContentCustomizationSerializer(color)
        logo, created = queryset.get_or_create(type='logo')
        logo_serializer = FullCustomizationSerializer(logo)
        sitename, created = queryset.get_or_create(type='sitename')
        sitename_serializer = FullCustomizationSerializer(sitename)
        data = {
            'background': background_serializer.data['file'],
            'color': color_serializer.data['content'],
             'logo': logo_serializer.data['file'],
            'sitename': sitename_serializer.data['content'],
        }
        return Response(data)

    def edit_file_item(self, request):
        file = request.data.get('file')
        queryset = Customization.objects.all()
        item = request.data.get('item')
        item, created = queryset.get_or_create(type=item)
        item.file.delete(save=True)
        if file != "null":
            item.file = file
            item.save()
        serializer = FullCustomizationSerializer(item)
        return Response(serializer.data['file'])

    def edit_item(self, request):
        new_value = request.data.get('value')
        item = request.data.get('item')
        queryset = Customization.objects.all()
        item, created = queryset.get_or_create(type=item)
        item.content = new_value
        item.save()
        serializer = FullCustomizationSerializer(item)
        return Response(serializer.data['content'])