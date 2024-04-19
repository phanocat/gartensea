from django.views.generic import TemplateView
from api.models import Customization

class IndexView(TemplateView):
    template_name = 'frontend/index.html'
    
    def get_context_data(self, * args, ** kwargs):
        context = super().get_context_data( * args, ** kwargs)
        context['title'] = Customization.objects.all().get(type='sitename').content
        context['logo'] = Customization.objects.all().get(type='logo').file
        return context
