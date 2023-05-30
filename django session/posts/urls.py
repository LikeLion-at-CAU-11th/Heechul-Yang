from django.urls import path, include
from posts.views import *
from . import views

from rest_framework.routers import DefaultRouter

# 1. Mixins

# urlpatterns = [
# 	path('', PostListMixins.as_view()),
# 	path('<int:pk>', PostDetailMixins.as_view()),
#     path('<int:pk>/comment', CommentListMixins.as_view()),
# 	path('comment/<int:pk>', CommentDetailMixins.as_view()),
# ]

# 2. Concrete Generic Views

# urlpatterns = [
#     path('', PostListGenericAPIView.as_view()),
#     path('<int:pk>', PostDetailGenericAPIView.as_view()),
#     path('<int:pk>/comment', CommentListGenericAPIView.as_view()),
#     path('comment/<int:pk>', CommentDetailGenericAPIView.as_view()),
# ]

# 3. ViewSet

# urlpatterns = [
#     path('', views.post_list),
#     path('<int:pk>', views.post_detail),
#     path('<int:pk>/comment', views.comment_list),
#     path('comment/<int:pk>', views.comment_detail),
# ]

# APIView

# urlpatterns = [
#     path('', PostList.as_view()),
#     path('<int:id>/', PostDetail.as_view()), 
#     path('<int:post_id>/comment', CommentInPost.as_view()),   
#     path('comment/<int:id>', CommentDetail.as_view()),    
# ]

router = DefaultRouter()
router.register(r'post', views.PostViewSet) # http://localhost:8000/posts/post & http://localhost:8000/posts/post/{post_id}
router.register('comment', views.CommentViewSet, basename='comment') # "http://localhost:8000/posts/comment & "http://localhost:8000/posts/comment/{comment_id}

urlpatterns = [
    path('',include(router.urls)),
]