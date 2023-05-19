from django.urls import path
from posts.views import *

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()), 
    path('<int:post_id>/comment', CommentInPost.as_view()),   
    path('comment/<int:id>', CommentDetail.as_view()),    
]