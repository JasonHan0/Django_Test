from django.contrib import messages  # 오류를 발생시키기 위해 messages 모듈을 이용
# messages는 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect    # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question
# pybo/views.py를 pybo/views/question_views.py로 분할 이동하여 .models, .forms가 ..models, ..forms로 바뀜
# pybo/views.py 파일에 있던 question_create, modify, delete 함수를 내용의 변경없이 그대로 복사함


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    # 동일한 URL 요청을 POST, GET 요청 방식에 따라 다르게 처리
    # 질문 목록 화면에서 "질문 등록하기" 버튼을 클릭한 경우에는 /pybo/question/create/ 페이지가 GET 방식으로 요청되어 question_create 함수가 실행
    # 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용
    #  request.method 값이 GET이 되어 if .. else .. 에서 else 구문을 타게 되어 결국 질문 등록 화면을 보여 주게 됨
    if request.method == 'POST':
        # POST 방식에서는 form = QuestionForm(request.POST) 처럼 request.POST를 인수로 생성
        form = QuestionForm(request.POST)
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid():                             # form이 유효한지 검사하고, 유효하다면 이후의 문장이 수행되어 질문 데이터가 생성 (DB에 insert하는 구문)
            # 만약 form에 저장된 subject, content의 값이 올바르지 않다면 form에는 오류 메시지가 저장되고 form.is_valid()가 실패하여 다시 질문 등록 화면 돌아감
            # 이 때 form에 저장된 오류 메시지는 질문 등록 화면에 표시
            # form으로 Question 데이터를 저장하기 위한 코드 // QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용
            question = form.save(commit=False)
            # commit=False는 임시 저장을 의미 // 실제 데이터는 아직 데이터베이스에 저장되지 않은 상태
            # 여기서 form.save(commit=False) 대신 form.save()를 수행하면 Question 모델의 create_date에 값이 없다는 오류가 발생
            # QuestionForm에는 현재 subject, content 속성만 정의되어 있고 create_date 속성은 없기 때문
            # 그래서 임시 저장을 한 후 question 객체를 리턴받아 create_date에 값을 설정한 후 question.save()로 실제 저장
            question.author = request.user  # author 속성에 로그인 계정 저장
            # 중요! // create_date 속성은 데이터 저장 시점에 자동 생성해야 하는 값이므로 QuestionForm에 등록하여 사용하지 않는다.
            question.create_date = timezone.now()
            question.save()
            # 저장이 완료되면 return redirect('pybo:index')를 호출하여 질문 목록 화면으로 이동
            return redirect('pybo:index')
    else:
        # GET 방식에서는 form = QuestionForm() 처럼 QuestionForm을 인수 없이 생성
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
# question_modify 함수는 로그인한 사용자(request.user)와 수정하려는 질문의 글쓴이(question.author)가 다를 경우에는 "수정권한이 없습니다"라는 오류를 발생
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        # instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        form = QuestionForm(request.POST, instance=question)
        # 질문 수정화면에서 제목 또는 내용을 변경하여 POST 요청하면 변경된 내용이 QuestionForm에 저장
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시는 현재일시로 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # GET 요청인 경우 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록
        form = QuestionForm(instance=question)
        # 폼 생성시 이처럼 instance 값을 지정하면 폼의 속성 값이 instance의 값으로 채워짐(질문을 수정하는 화면에서 제목과 내용이 채워진 채로 보임)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

    # ※ form 태그에 action 속성이 없는 경우 디폴트 action은 현재 페이지가 된다.
    # ※ 질문 수정화면에서 사용한 템플릿은 질문 등록시 사용했던 pybo/question_form.html 파일과 동일

# question_delete 함수 역시 로그인이 필요하므로 @login_required 애너테이션을 적용, 로그인한 사용자와 작성자가 동일한 경우에만 삭제할 수 있도록 함


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
