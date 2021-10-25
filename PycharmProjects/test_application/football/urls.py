from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('competitions', views.competitions, name='competitions'),
    path('scorers', views.scorers, name='scorers'),

]