import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# 이 파일에 선언된 application이 바로 장고의 애플리케이션
# 이 파일은 장고 프로젝트 생성시 자동으로 만들어지며 특별한 경우가 아니고는 수정할 필요 없음


# WSGI 서버는 웹서버가 동적 페이지 요청을 처리하기 위해 호출하는 서버
#1. WSGI 서버에는 여러 종류가 있지만 uwsgi와 Gunicorn을 가장 많이 사용 (파이보에서는 Gunicorn 사용 연습)
#2. 웹서버에 동적 페이지 요청이 발생하면 웹 서버는 WSGI 서버를 호출하고 WSGI 서버는 다시 WSGI 애플리케이션을 호출
#3. 여기서 알수 있는 중요한 사실은 실제 동적 페이지 요청은 결국 WSGI 애플리케이션이 처리
#4. WSGI 애플리케이션에는 장고(Django), 플라스크(Flask), 토네이도(Tornado)
#5. 파이보 시스템이 사용할 WSGI 애플리케이션은 장고
#6. WSGI 서버는 웹 서버와 WSGI 애플리케이션 중간에 위치, 그래서 WSGI 서버는 WSGI 미들웨어(middleware) 또는 WSGI 컨테이너(container)
#7. WSGI 서버는 항상 "wsgi.py" 파일을 경유하여 장고(django) 프로그램을 호출
