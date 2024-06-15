from django.views.generic import TemplateView
from api.models import Customization, Post, Article, Image
from django.shortcuts import render, get_object_or_404, redirect
from bs4 import BeautifulSoup

class IndexView(TemplateView):
    template_name = 'frontend/index.html'
    
    def get_context_data(self, * args, ** kwargs):
        context = super().get_context_data( * args, ** kwargs)
        queryset = Customization.objects.all()
        sitename, created = queryset.get_or_create(type='sitename')
        if sitename.content == '':
            title = 'Gartensea'
        else:
            title = sitename.content
        context['title'] = title
        logo, created = queryset.get_or_create(type='logo')
        context['logo'] = logo.file
        return context

class InfoView(TemplateView):
    template_name = 'frontend/portal-info.html'
    
    def get_context_data(self, * args, ** kwargs):
        context = super().get_context_data( * args, ** kwargs)
        queryset = Customization.objects.all()
        permission, created = queryset.get_or_create(type='subscribePermission')
        if permission.content == '':
            permission.content = 'true'
            permission.save()
        if permission == 'true':
            sitename, created = queryset.get_or_create(type='sitename')
            context['title'] = sitename.content
            logo, created = queryset.get_or_create(type='logo')
            context['logo'] = logo.file
            context['last_post_id'] = Post.objects.latest('id').id
            context['last_article_id'] = Article.objects.latest('id').id
            context['logo'] = logo.file
        else:
            context['title'] = 'Closed Gartensea Page'
        return context
        
def post_item(request, id):
    post = get_object_or_404(Post, id=id)
    text = post.text
    text = text[:180] + '...' if len(text) > 180 else text
    cleantext = BeautifulSoup(text, "html.parser").text
    if Image.objects.filter(post=post).exists():
        cover = Image.objects.filter(post=post).latest('id').file
    else:
        logo, created = Customization.objects.all().get_or_create(type='logo')
        cover = logo.file
    sitename, created = Customization.objects.all().get_or_create(type='sitename')
    if sitename.content == '':
        sitename = 'Гортензия'
    else:
        sitename = sitename.content
    context = {
        'id': id,
        'sitename': sitename,
        'text': cleantext,
        'cover': cover,
    }
    return render(request, 'frontend/item.html', context=context)