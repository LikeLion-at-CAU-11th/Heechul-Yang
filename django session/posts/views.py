from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post


# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse(
            {
                'status' : 200,
                'success' : True,
                'message' : '메시지 전달 성공!',
                'data' : 'Hello, World!',
            }
        )
@require_http_methods(["GET"])      
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk = id)
    
    category_json = {
        "id" : post.pk,
        "writer" : post.writer,
        "content" : post.content,
        "category" : post.category,
    }
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : category_json,
    })
   
@require_http_methods(["GET"])     
def get_post_detail_all(request):
            
    category_obj = Post.objects.all()
    
    
    category_list = []
    
    for post in category_obj:
        
        post_data = {
            "id" : post.pk,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        }        
        
        post_json = json.dumps(post_data)
        category_list.append(post_json) 
        
    # category_list = serializers.serialize('json', category_obj)
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : category_list,
    })