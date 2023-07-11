from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post, Comment
from accounts.models import Member
import datetime as dt
from .serializers import PostSerializer, CommentSerializer, ResisterSerializer, AuthSerializer

#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# JWT
from rest_framework_simplejwt.serializers import RefreshToken
    
# 인가
from rest_framework import permissions
from config.permissions import IsWriterOrReadOnly

# APIView (post)

class PostList(APIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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
    
    permission_classes = [IsWriterOrReadOnly]    
    
    def get_object(self, id):
        post = Post.objects.get(id=id)
        self.check_object_permissions(self.request, post)
        return post
    
    def get(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post)
        return Response(serializers.data)
    
    def put(self, request, id):
        post = self.get_object(id = id)
        serializers = PostSerializer(post, data=request.data) # 전달받은 값으로 수정하여 직렬화
        if serializers.is_valid(): # 유효성 검토
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = self.get_object(id = id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# APIView (comment)

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
    
# 인증/인가

class RegisterView(APIView):
    serializer_class = ResisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            member = serializer.save(request)
            token = RefreshToken.for_user(member)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            res = Response(
                {
                    "member" : serializer.data,
                    "message" : "register success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status= status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    serializer_class = AuthSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            member = serializer.validated_data["member"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            
            res = Response(
                {
                    "member" : {
                        "id" : member.id,
                        "email" : member.email,
                        "age" : member.age,
                    },
                    "message" : "login success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status = status.HTTP_200_OK
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        res = Response({
            "message" : "logout success"
        }, status=status.HTTP_202_ACCEPTED)
        
        res.delete_cookie("access-token")
        res.delete_cookie("refresh-token")
        return res