from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post, Comment
import datetime as dt
from .serializers import PostSerializer, CommentSerializer

#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework import mixins
from rest_framework import generics

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

# post

# 1. Mixins
# queryset을 리스트로 만들어 주거나 저장 혹은 수정 후 Save해주는 과정 등 기본적인 CRUD가 구현되어 있음

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs): # *args(dict 제외) **kargs(dict 형태만) 는 어떤 형태의 인자든 모두 받겠다는 뜻
        return self.list(request)
    
    def post(self, request, *args, **kwargs): 
        return self.create(request, *args, **kwargs)
    
class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs): 
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# 2. Concrete Generic Views
# Mixins 보다 상속 클래스가 적어짐

class PostListGenericAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
# 3. ViewSet
# 공통적으로 반복되는 queryset과 serializer를 한 번만 사용해도 됨

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
# post_list = PostViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create',
# })

# post_detail = PostViewSet.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy',
# })
# 라우팅을 위한 코드
    
# APIView

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data) # 클라이언트가 보낸 값을 직렬화 (JSON으로) 해서 저장
        if serializer.is_valid(): # 유효성 검토
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) # 다수의 객체 직렬화 -> many = True
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id = id)
        serializers = PostSerializer(post)
        return Response(serializers.data)
    
    def put(self, request, id):
        post = get_object_or_404(Post, id = id)
        serializers = PostSerializer(post, data=request.data) # 전달받은 값으로 수정하여 직렬화
        if serializers.is_valid(): # 유효성 검토
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, id = id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ** Comment **

# Mixins

class CommentListMixins(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class CommentDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# 2. Concrete Generic Views

class CommentListGenericAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class CommentDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
# 3. ViewSet

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
  
# 라우팅  

# comment_list = CommentViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create',
# })

# comment_detail = CommentViewSet.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy',
# })

# APIView

class CommentInPost(APIView):
    
    def get(self, request, post_id): # 특정 post에 달린 모든 comment 가져오기
        comment = Comment.objects.filter(post = post_id)
        serializers = CommentSerializer(comment, many=True)
        return Response(serializers.data)
    
    def post(self, request, post_id):
        request.data["post"] = post_id # url로 전달 받은 post_id를 생성 시 post필드에 삽입
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CommentDetail(APIView):
    
    def get(self, request, id):
        comment = get_object_or_404(Comment, id = id) # comment의 id로 특정한 comment 가져오기
        serializers = CommentSerializer(comment)
        return Response(serializers.data)
    
    def put(self, request, id):
        comment = get_object_or_404(Comment, id = id)
        serializers = CommentSerializer(comment, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        comment = get_object_or_404(Comment, id = id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
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
    