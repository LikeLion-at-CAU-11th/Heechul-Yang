from django.urls import path
from introduction.views import *

urlpatterns = [
    path('', introduce, name='introduce'),
]
