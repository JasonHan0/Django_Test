from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'),
         name='login'),    # 로그인 뷰는 따로 만들 필요없이 django.contrib.auth 앱의 LoginView를 사용
    # LoginView가 common 디렉터리의 템플릿을 참조할 수 있도록 template_name='common/login.html' 추가
    # 이제 common/login.html 파일을 생성
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 로그아웃 시 리다이렉트할 위치도 config/settings.py 파일에 추가
]
