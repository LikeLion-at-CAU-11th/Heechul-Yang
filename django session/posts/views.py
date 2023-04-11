from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post, Comment
import datetime as dt


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
@require_http_methods(["GET", "PATCH", "DELETE"])      
def post_detail(request, id):
    if request.method == "GET":
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
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk=id)

        update_post.content = body['content']
        update_post.category = body['category']
        
        update_post.save()
        
        update_post_json = {
            "id" : update_post.id,
            "writer" : update_post.writer,
            "content" : update_post.content,
            "category" : update_post.category,
        }
        
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 수정 성공',
            'data' : update_post_json
        })
    elif request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()
        
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 삭제 성공',
            'data' : None
        })
        
   
@require_http_methods(["GET"])     
def get_post_all(request):
    
    category_obj = Post.objects.all()

    category_list = []

    for post in category_obj:

        post_data = {
            "id" : post.pk,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        }        

        # post_json = json.dumps(post_data) 
        # post를 직접 json.dumps하니 json변환이 제대로 이루어지지 않음.
        category_list.append(post_data) 

    # category_list = serializers.serialize('json', category_obj)
    # 근데 category_obj를 통째로 serialize하는 건 문제없이 작동됨. -> 왜?
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : category_list,
    })
    
    
@require_http_methods(['POST'])    
def create_post(request):
    body = json.loads(request.body.decode('utf-8'))
    
    new_post = Post.objects.create(
           writer = body['writer'],
           content = body['content'],
           category = body['category']
       )
    
    new_post_json = {
           "id" : new_post.id,
           "writer" : new_post.writer,
           "content" : new_post.content,
           "category" : new_post.category
       }
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 생성 성공',
        'data' : new_post_json
    })
    
@require_http_methods(["GET"])
def get_comment(request, id):
    comment_all = Comment.objects.filter(post = id)
    
    comment_json_list = []
    
    for comment in  comment_all:
        comment_json = {
            "writer" : comment.writer,
            "content" : comment.content
        }
        
        comment_json_list.append(comment_json)
        
    return JsonResponse({
        'status' : 200,
        "message" : '코멘트 조회 성공',
        'data' : comment_json_list
    })

@require_http_methods(["POST"])
def create_comment(request, post_id):
    body = json.loads(request.body.decode('utf-8'))
    
    new_comment = Comment.objects.create(
        writer = body['writer'],
        content = body['content'],
        post_id = post_id  # FK
    )
    
    new_comment_json = {
        "writer" : new_comment.writer,
        "content" : new_comment.content,
    }
    
    return JsonResponse({
        'status' : 200,
        'message' : '코멘트 생성 성공',
        'data' : new_comment_json
    })
    
@require_http_methods(["GET"])
def get_recent_post(request):
    post_all = Post.objects.all()
    
    recent_post_list = []
    
    before = dt.datetime(2023, 4, 5, 22, 0) # 5주차 세션 마무리 시간
    after = dt.datetime(2023, 4, 12, 19, 0) # 6주차 세션 시작 시간
    
    for post in post_all:
        post_created_time = post.created_at.replace(tzinfo=None)
        # 시간 비교를 위해 naive형식으로 변환
        # aware형식으로 통일하려면 pytz.timezone 사용 가능 (pytz pip 필요)
        
        if post_created_time > before and post_created_time < after:
            
            post_json = {
                "id" : post.pk,
                "writer" : post.writer,
                "content" : post.content,
                "category" : post.category
            }
            
            recent_post_list.append(post_json)
            
    return JsonResponse({
        'status' : 200,
        'message' : '최근 포스트 조회 성공',
        "data" : recent_post_list
    })