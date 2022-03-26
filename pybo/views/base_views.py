from django.core.paginator import Paginator     # 페이징을 위해 사용하는 클래스
from django.shortcuts import render, get_object_or_404  # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수

from ..models import Question
# pybo/views.py를 pybo/views/base_views.py로 분할 이동하여 .models가 ..models로 바뀜
# pybo/views.py 파일에 있던 index함수와 detail 함수를 내용의 변경없이 그대로 복사함

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # http://localhost:8000/pybo/?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올 때 사용
    page = request.GET.get('page', '1')
    # 만약 http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정
    # 조회
    question_list = Question.objects.order_by(
        '-create_date')        # 질문 목록 데이터 / 작성일시 역순으로 정렬

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    max_index = len(paginator.page_range)     # 마지막 페이지
    # 첫 번째 파라미터 question_list는 게시물 전체를 의미하는 데이터이고 두번째 파라미터 10은 페이지당 보여줄 게시물의 개수
    # 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성
    page_obj = paginator.get_page(page)
    # 장고 내부적으로 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경

    # 위의 페이징 처리 내용을 위해 컨텍스트에 추가
    context = {'question_list': page_obj, 'max_index': max_index}
    # context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


# def detail(request, question_id):
#     """
#     pybo 내용 출력
#     """
#     question = Question.objects.get(id=question_id)
#     context = {'question': question}
#     return render(request, 'pybo/question_detail.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

# question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())     # POST로 전송된 폼(form) 데이터 항목 중 content 값을 의미
