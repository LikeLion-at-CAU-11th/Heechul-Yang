from django.urls import path
from posts.views import *

urlpatterns = [
    path('',code_review, name="code_review")
]
