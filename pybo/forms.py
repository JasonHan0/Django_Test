"""
#{{ form.as_p }}를 사용하면 빠르게 템플릿을 만들 수 있지만 HTML 코드가 자동으로 생성되므로 디자인 측면에서 많은 제한이 생기게 된다. 
예를 들어 특정 태그를 추가하거나 필요한 클래스를 추가하는 작업에 제한이 생긴다. 
또 디자인 영역과 서버 프로그램 영역이 혼재되어 웹 디자이너와 개발자의 역할을 분리하기도 모호해진다.
폼을 이용하여 자동으로 HTML 코드를 생성하지 말고 직접 HTML 코드를 작성하는 방법을 사용해 보자.
우선 수작업에 불 필요한 forms.py 파일의 widget 항목을 제거
"""
from django import forms
from pybo.models import Question, Answer

# 화면을 깔끔하게 만들어 줄 수 있는 부트스트랩을 준비
# 하지만 {{ form.as_p }} 태그는 HTML 코드를 자동으로 생성하기 때문에 부트스트랩을 적용할 수가 없음


class QuestionForm(forms.ModelForm):        # forms.ModelForm을 상속
    # 장고의 폼은 일반 폼(forms.Form)과 모델 폼(forms.ModelForm)이 있는데 모델 폼은 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼이다.
    # 모델 폼은 이너 클래스인 Meta 클래스가 반드시 필요하다.
    # Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.

    # 즉, QuestionForm은 Question 모델과 연결된 폼이고 속성으로 Question 모델의 subject와 content를 사용한다고 정의한 것이다.
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {       # Meta 클래스의 widgets 속성을 지정하면 입력 필드에 form-control과 같은 부트스트랩 클래스를 추가할 수 있음
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
# class Userlistentime(forms.ModelForm):
#     class Meta:
#         model = Music  # 사용할 모델
#         fields = ['song', 'artists', 'listen_time', 'asdjlfkjsda']
