from django.urls import path

from . import models
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', models.list),
    path('create', models.create),
    path('read/<int:recordId>', models.read),
    path('debug/<int:recordId>', models.debug),
    path('modify/<int:recordId>', models.modify),
    path('remove/<int:recordId>', models.remove),
    ]

