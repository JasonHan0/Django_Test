# from django.http import HttpResponse 
from django.shortcuts import render, get_object_or_404, redirect      # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator     # 페이징을 위해 사용하는 클래스
from django.contrib.auth.decorators import login_required
"""
request.user가 User 객체가 아닌 AnonymousUser 객체
request.user에는 로그아웃 상태이면 AnonymousUser 객체가, 로그인 상태이면 User 객체가 들어있는데, 앞에서 우리는 author 속성을 정의할 때 User를 이용하도록 되어 있음
그래서 answer.author = request.user에서 User 대신 AnonymousUser가 대입되어 오류가 발생
문제를 해결하려면 request.user를 사용하는 함수에 @ login_required 애너테이션을 사용해야 함(로그인이 필요한 함수를 의미)
answer_create 함수와 question_create 함수는 함수내에서 request.user를 사용하므로 로그인이 필요한 함수
로그아웃 상태에서 @login_required 어노테이션이 적용된 함수가 호출되면 자동으로 로그인 화면으로 이동
@login_required 어노테이션은 login_url='common:login' 처럼 로그인 URL을 지정할 수 있음
"""

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # http://localhost:8000/pybo/?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올 때 사용
                                         # 만약 http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정
    # 조회
    question_list = Question.objects.order_by('-create_date')        # 질문 목록 데이터 / 작성일시 역순으로 정렬

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기    
    max_index = len(paginator.page_range)     # 마지막 페이지
    # 첫 번째 파라미터 question_list는 게시물 전체를 의미하는 데이터이고 두번째 파라미터 10은 페이지당 보여줄 게시물의 개수
    page_obj = paginator.get_page(page)       # 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성
    # 장고 내부적으로 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경

    context = {'question_list': page_obj,'max_index': max_index}    # 위의 페이징 처리 내용을 위해 컨텍스트에 추가
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
            return redirect('pybo:detail', question_id=question.id)
    else:   # 답변 등록은 POST 방식만 사용되기 때문에 if .. else 구문에서 else는 호출되지 않음 //  다만, 여기에서는 패턴의 통일성을 위해 남겨 둠
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)  


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
        form = QuestionForm(request.POST)   # POST 방식에서는 form = QuestionForm(request.POST) 처럼 request.POST를 인수로 생성
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid():                             # form이 유효한지 검사하고, 유효하다면 이후의 문장이 수행되어 질문 데이터가 생성 (DB에 insert하는 구문)
            # 만약 form에 저장된 subject, content의 값이 올바르지 않다면 form에는 오류 메시지가 저장되고 form.is_valid()가 실패하여 다시 질문 등록 화면 돌아감 
            # 이 때 form에 저장된 오류 메시지는 질문 등록 화면에 표시
            question = form.save(commit=False)          # form으로 Question 데이터를 저장하기 위한 코드 // QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용
                        # commit=False는 임시 저장을 의미 // 실제 데이터는 아직 데이터베이스에 저장되지 않은 상태
                        # 여기서 form.save(commit=False) 대신 form.save()를 수행하면 Question 모델의 create_date에 값이 없다는 오류가 발생
                        # QuestionForm에는 현재 subject, content 속성만 정의되어 있고 create_date 속성은 없기 때문
                        # 그래서 임시 저장을 한 후 question 객체를 리턴받아 create_date에 값을 설정한 후 question.save()로 실제 저장       
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 중요! // create_date 속성은 데이터 저장 시점에 자동 생성해야 하는 값이므로 QuestionForm에 등록하여 사용하지 않는다.  
            question.save()
            return redirect('pybo:index')   #  저장이 완료되면 return redirect('pybo:index')를 호출하여 질문 목록 화면으로 이동            
    else:
        form = QuestionForm()           # GET 방식에서는 form = QuestionForm() 처럼 QuestionForm을 인수 없이 생성
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

