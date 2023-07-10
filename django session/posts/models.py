from django.db import models
from accounts.models import Member
from django.conf import settings

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True
    
class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )
    # text입력이 아닌 선택형 입력으로 만듬

    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    # CharField 에는 max_length 속성 필수!!

class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)
    # 참조 받을 테이블 (FK)