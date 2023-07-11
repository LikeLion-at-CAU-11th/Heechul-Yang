from rest_framework import serializers
from .models import Post, Comment
from accounts.models import Member
from rest_framework_simplejwt.serializers import RefreshToken

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        
class ResisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    email = serializers.CharField(required = True)
    age = serializers.IntegerField(required = True)
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'email', 'age']
        
    # 회원 정보 저장    
    def save(self, request):
        
        member = Member.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            age = self.validated_data['age'],
        )
        
        # password는 별도로 암호화
        member.set_password(self.validated_data["password"])
        
        member.save()
        
        return member
    
    # 중복 회원 가입 검사
    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        
        if Member.objects.filter(email = email).exists():
            raise serializers.ValidationError('email already exists')
        if Member.objects.filter(username = username).exists():
            raise serializers.ValidationError('username already exists')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = Member
        fields = ["username", "password"]
        
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        
        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)
              
            if not member.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("member account not exist")
		        
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)
		
        data = {
				'member':member,
				'refresh_token':refresh_token,
				'access_token':access_token,
		}
		
        return data
        
# 가져올 필드를 지정해줄 수도 있다.
# fields = ['writer', 'content']

# 제외할 필드를 지정해줄 수도 있다.		
# exclude = ['id']

# create, update, delete는 안되고 read만 되는 필드를 선언할 수도 있다.(이름같이 변경되지 않아야하는 필드의 경우)
# read_only_fields = ['writer']