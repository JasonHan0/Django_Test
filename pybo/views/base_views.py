from django.core.paginator import Paginator     # 페이징을 위해 사용하는 클래스
from django.shortcuts import render, get_object_or_404  # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
from ..models import Question
# pybo/views.py를 pybo/views/base_views.py로 분할 이동하여 .models가 ..models로 바뀜
# pybo/views.py 파일에 있던 index함수와 detail 함수를 내용의 변경없이 그대로 복사함
from django.db.models import Q, Count  # Q함수는 OR조건으로 데이터를 조회하기 위해 사용하는 함수
# 전달한 so 파라미터로 질문 목록을 정렬할 수 있도록 index함수 수정
# 추천수는 장고의 annotate를 이용하여 Count함수를 사용


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # http://localhost:8000/pybo/?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올 때 사용
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        # 1. 정렬기준이 추천순(recommend)인 경우는 추천수가 큰것부터 정렬해야 하므로 order_by에 추천수에 해당되는 -num_voter가 추가
        # 2. Question.objects.annotate(num_voter=Count('voter'))는 Question의 기존 속성인 author, subject, content, create_date, modify_date, voter에 
                                                                                                        # num_voter라는 속성을 하나 더 추가한다고 생각
        # 3. annotate로 num_voter를 지정하면 filter나 order_by에서 num_voter를 사용 가능
        # 4. 질문의 추천수인 num_voter는 Count('voter') 처럼 Count 함수를 사용하여 얻을 수 있음
        # 5. Count('voter') 는 이 질문의 추천수를 의미
        # 6. order_by('-num_voter', '-create_date') 처럼 order_by 함수에 1개 이상의 파라미터가 전달될 때는 
        # 앞의 항목부터 우선순위를 갖게 되어 추천수로 먼저 정렬하고 추천수가 같을경우에는 최신순으로 정렬
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 만약 http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정
    # 조회
    # question_list = Question.objects.order_by('-create_date')     # 질문 목록 데이터 / 작성일시 역순으로 정렬
    if kw:
        question_list = question_list.filter(
            # filter 함수에서 모델 속성에 접근하기 위해서는 이처럼 __ (언더바 두개) 를 이용하여 하위 속성에 접근 가능
            Q(subject__icontains=kw) |  # 제목검색
            # Q함수내에 사용된 subject__icontains=kw의 의미는 제목에 kw 문자열이 포함되었는지를 의미
            # subject__contains=kw 대신 subject__icontains=kw을 사용하면 대소문자를 가리지 않고 찾기 가능
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
            # answer__author__username__icontains 은 좀 복잡해 보이는데 "답변을 작성한 사람의 이름에 포함되는가?" 라는 의미
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    max_index = len(paginator.page_range)     # 마지막 페이지
    # 첫 번째 파라미터 question_list는 게시물 전체를 의미하는 데이터이고 두번째 파라미터 10은 페이지당 보여줄 게시물의 개수
    # 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성
    page_obj = paginator.get_page(page)
    # 장고 내부적으로 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경

    # 위의 페이징 처리 내용 및 검색을 위해 컨텍스트에 추가
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # page, kw, so 값을 템플릿에 전달하기 위해 context 딕셔너리에 추가
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
