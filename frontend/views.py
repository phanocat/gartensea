from django.views.generic import TemplateView
from api.models import Customization, Post, Article

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
        sitename, created = queryset.get_or_create(type='sitename')
        context['title'] = sitename.content
        logo, created = queryset.get_or_create(type='logo')
        context['logo'] = logo.file
        context['last_post_id'] = Post.objects.latest('id').id
        context['last_article_id'] = Article.objects.latest('id').id
        return context
