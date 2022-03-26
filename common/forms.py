from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# UserForm을 따로 만들지 않고 UserCreationForm을 그대로 사용해도 되지만 위처럼 이메일 등의 부가 속성을 추가하기 위해서는 UserCreationForm 클래스를 상속하여 만들어야 함
class UserForm(UserCreationForm):  # django.contrib.auth.forms 모듈의 UserCreationForm 클래스를 상속
    email = forms.EmailField(label="이메일")        # email 속성을 추가

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
