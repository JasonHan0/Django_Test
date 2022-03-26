from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):    # POST 요청인 경우에는 화면에서 입력한 데이터로 사용자를 생성하고 GET 요청인 경우에는 계정생성 화면을 리턴
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # form.cleaned_data.get 함수는 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수로 여기서는 사용자명과 비밀번호를 얻기 위해 사용
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 신규 사용자를 생성한 후에 자동 로그인 될 수 있도록 authenticate와 login함수가 사용(django.contrib.auth 모듈의 함수로 사용자 인증과 로그인을 담당)
            user = authenticate(username=username,  # authenticate 함수는 사용자명과 비밀번호가 정확한지 검증하는 함수
                                password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            # 계정생성 화면을 구성하는 templates/common/signup.html 템플릿 작성 필요
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
