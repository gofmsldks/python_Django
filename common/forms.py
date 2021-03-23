from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일") # 폼에 이메일 추가 , User model에도 들어감

    class Meta:
        model = User
        fields = ("username", "email") # 관리자페이지 등에서 보여줄수 있는 속성 (회원 목록에서 이름하고 이메일만 보여줌) 개별적으로 정해짐