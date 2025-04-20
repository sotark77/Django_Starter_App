from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('blogs/', blog_list, name='blogs_list'),
    path('blog/', blog_view, name='blog_view'),
]