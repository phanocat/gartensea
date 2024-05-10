from django.views.generic import TemplateView
from api.models import Customization, Post, Article

class IndexView(TemplateView):
    template_name = 'frontend/index.html'
    
    def get_context_data(self, * args, ** kwargs):
        context = super().get_context_data( * args, ** kwargs)
        context['title'] = Customization.objects.all().get(type='sitename').content
        context['logo'] = Customization.objects.all().get(type='logo').file
        return context

class InfoView(TemplateView):
    template_name = 'frontend/portal-info.html'
    
    def get_context_data(self, * args, ** kwargs):
        context = super().get_context_data( * args, ** kwargs)
        context['title'] = Customization.objects.all().get(type='sitename').content
        context['logo'] = Customization.objects.all().get(type='logo').file
        context['last_post_id'] = Post.objects.latest('id').id
        context['last_article_id'] = Article.objects.latest('id').id
        return context
