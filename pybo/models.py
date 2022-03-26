from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    # Question 모델에 author 속성을 추가
    author = models.ForeignKey(       
        User, on_delete=models.CASCADE, related_name='author_question') # related_name 인수를 추가하여 User 모델에서 author와 voter를 구별하게 해줌
                                                                        #이제 특정 사용자가 작성한 질문을 얻기 위해서는 some_user.author_question.all() 처럼 사용할 수 있음
    # author 필드는 User 모델을 ForeignKey로 적용하여 선언
    # User 모델은 django.contrib.auth 앱이 제공하는 사용자 모델
    # on_delete=models.CASCADE는 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제하라는 의미
    # author 속성에 저장해야 하는 사용자 객체는 로그인 후 request 객체를 통해 얻을 수 있음
    # 계정 생성시마다 id가 1부터 순차적으로 증가(Auto Increment) 따라서 우리가 createsuperuser로 최초 생성했던 계정인 root의 id 값은 1
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)   # 수정 일시를 의미하는 modify_date 속성
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    # 하나의 질문에 여러명이 추천할 수 있고 한 명이 여러 개의 질문에 추천할 수 있으므로 이런 경우에는 "다대다(N:N)" 관계를 의미하는 ManyToManyField를 사용
    def __str__(self):
        return self.subject
    
    # class Meta:
    #     db_table = 'haha'


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='author_answer')  # Answer 모델에 author 속성을 추가
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)   # 수정 일시를 의미하는 modify_date 속성
    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미
    # blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미
    # 즉, null = True, blank = True는 어떤 조건으로든 값을 비워둘 수 있음을 의미(수정일시는 수정한 경우에만 생성되는 데이터이므로)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):    # 댓글 모델
    author = models.ForeignKey(User, on_delete=models.CASCADE)          # 댓글 글쓴이
    # question, answer 속성에는 질문이나 답변이 삭제될 경우에 해당 댓글도 삭제될 수 있도록 on_delete=models.CASCADE 옵션을 설정
    content = models.TextField()                                        # 댓글 내용
    create_date = models.DateTimeField()                                # 댓글 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)           # 댓글 수정일시
    # 댓글 모델의 question 또는 answer 둘 중에 하나에만 값이 저장되므로 두 개의 속성은 모두 null=True, blank=True 를 설정
    question = models.ForeignKey(                                       # 이 댓글이 달린 질문
        Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(                                         # 이 댓글이 달린 답변
        Answer, null=True, blank=True, on_delete=models.CASCADE)
