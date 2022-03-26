import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter    # sub 함수에 @register.filter 애너테이션을 적용하면 템플릿에서 해당 함수를 필터로 사용
def sub(value, arg):
    return value - arg      # sub 필터는 기존 값 value에서 입력으로 받은 값 arg를 빼서 리턴


@register.filter()
def mark(value):    # mark 함수는 markdown 모듈과 mark_safe 함수를 이용하여 입력 문자열을 HTML로 변환하는 필터 함수
    extensions = ["nl2br", "fenced_code"]
    # nl2br은 줄바꿈 문자를 <br> 로 바꿔주고, fenced_code는 리스트, 강조, 링크, 소스코드, 인용 표현을 위해 필요
    # nl2br을 사용하지 않을 경우 줄바꿈을 하기 위해서는 줄 끝에 스페이스(' ')를 두개 연속으로 입력
    return mark_safe(markdown.markdown(value, extensions=extensions))
