from django.contrib import messages  # 오류를 발생시키기 위해 messages 모듈을 이용
# messages는 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect    # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment
# pybo/views.py를 pybo/views/comment_views.py로 분할 이동하여 .models, .forms가 ..models, ..forms로 바뀜
# pybo/views.py 파일에 있던 comment_create(modify, delete)_question/answer 함수를 내용의 변경없이 그대로 복사함


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            # 질문에 대한 댓글이므로 comment.question = question 처럼 comment에 question을 저장
            comment.question = question
            comment.save()
            # 댓글이 저장된 후에는 댓글을 작성한 질문 상세(pybo:detail) 화면으로 리다이렉트
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 질문에 등록된 댓글을 수정하기 위한 comment_modify_question 함수 추가


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

# GET 방식이면 기존 댓글을 조회하여 폼에 반영하고 POST 방식이면 입력된 값으로 댓글을 업데이트
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()    # 업데이트 시 modify_date에 수정일시를 반영
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 질문에 등록된 댓글을 삭제하는 함수 comment_delete_question 추가


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        # 댓글 삭제 권한이 없을 시 댓글이 있던 상세 화면으로 리다이렉트
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    # 댓글 삭제 시 댓글이 있던 상세 화면으로 리다이렉트
    return redirect('pybo:detail', question_id=comment.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
            # 답변의 댓글인 경우 question_id 값을 알기 위해 comment.answer.question 처럼 답변(answer)을 통해 질문(question)을 얻을 수 있도록 함
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)
