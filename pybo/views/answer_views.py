from django.contrib import messages  # 오류를 발생시키기 위해 messages 모듈을 이용
# messages는 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url    # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer
# pybo/views.py를 pybo/views/answer_views.py로 분할 이동하여 .models, .forms가 ..models, ..forms로 바뀜
# pybo/views.py 파일에 있던 answer_create, modify, delete 함수를 내용의 변경없이 그대로 복사함


@login_required(login_url='common:login')   # 로그인이 필요한 함수를 의미
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())  # POST로 전송된 폼(form) 데이터 항목 중 content 값을 의미
    # answer.save()
    # return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장 // 질문, 답변에 글쓴이를 추가
            # 답변의 글쓴이는 현재 로그인한 계정이므로 answer.author = request.user로 처리, request.user는 현재 로그인한 계정의 User 모델 객체
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))  # 답변을 등록하거나 수정할 때  html에서 지정한 앵커 태그로 이동하도록 코드 수정
            # pybo:detail URL에 #answer_2와 같은 앵커를 추가하기 위해 resolve_url 함수(실제 호출되는 URL 문자열을 리턴)를 사용
    else:   # 답변 등록은 POST 방식만 사용되기 때문에 if .. else 구문에서 else는 호출되지 않음 //  다만, 여기에서는 패턴의 통일성을 위해 남겨 둠
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# views.answer_delete 함수 정의


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
