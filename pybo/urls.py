from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    # /pybo URL은 config/urls.py 파일에 매핑된 pybo/ 와 pybo/urls.py 파일에 매핑된 '' 이 더해져 views.index 함수와 매핑
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),  
    # 댓글을 등록할 경우에는 답변 id 번호(<int:answer_id>)를 사용
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'), 
    # 댓글을 수정하거나 삭제할 경우에는 댓글의 id번호(<int:comment_id>)를 사용
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
]

