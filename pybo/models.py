from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)      # Question 모델에 author 속성을 추가
    # author 필드는 User 모델을 ForeignKey로 적용하여 선언
    # User 모델은 django.contrib.auth 앱이 제공하는 사용자 모델
    # on_delete=models.CASCADE는 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제하라는 의미
    # author 속성에 저장해야 하는 사용자 객체는 로그인 후 request 객체를 통해 얻을 수 있음
    # 계정 생성시마다 id가 1부터 순차적으로 증가(Auto Increment) 따라서 우리가 createsuperuser로 최초 생성했던 계정인 root의 id 값은 1
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject
    
    # class Meta:
    #     db_table = 'haha'


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Answer 모델에 author 속성을 추가
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()