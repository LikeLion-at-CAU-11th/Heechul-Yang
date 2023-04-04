from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('post_detail/<int:id>/', get_post_detail, name='get_post_detail'),
    path('post_detail_all/', get_post_detail_all, name="get_post_detail_all"), 
]