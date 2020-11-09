from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='gui-home'),
    path('figure.html', views.graph, name='gui-graph'),
]
