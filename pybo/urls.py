from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
]
# /pybo URL은 다음처럼 config/urls.py 파일에 매핑된 pybo/ 와 pybo/urls.py 파일에 매핑된 '' 이 더해져 views.index 함수와 매핑

