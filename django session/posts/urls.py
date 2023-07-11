from django.urls import path, include
from posts.views import *
from . import views

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()), 
    path('<int:post_id>/comment', CommentInPost.as_view()),   
    path('comment/<int:id>', CommentDetail.as_view()),    
    # 인증
    path('join', RegisterView.as_view()),
    path('login', AuthView.as_view()),
    # 토큰
    # path('token', TokenObtainPairView.as_view(), name = "toke_obtain_pair"),
    # path('token/refresh', TokenRefreshView.as_view(), name = "token_refresh"),
    # path('token/verify', TokenVerifyView.as_view(), name = "token_verify"),
]