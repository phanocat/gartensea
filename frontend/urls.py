from django.urls import path, re_path
from .views import *


urlpatterns = [
    re_path('portal-info', InfoView.as_view()),
    path('post-item/<int:id>', post_item),
    re_path(r'^', IndexView.as_view()),
]

