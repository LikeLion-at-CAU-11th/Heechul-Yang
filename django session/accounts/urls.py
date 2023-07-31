from django.urls import path, include
from posts.views import *
from accounts.views import *
from . import views

urlpatterns = [ 
    # 인증
    path('join', RegisterView.as_view()),
    path('login', AuthView.as_view()),
    # 토큰
    # path('token', TokenObtainPairView.as_view(), name = "toke_obtain_pair"),
    # path('token/refresh', TokenRefreshView.as_view(), name = "token_refresh"),
    # path('token/verify', TokenVerifyView.as_view(), name = "token_verify"),
    # 구글 소셜로그인
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]