from .base import *
# 서버 환경을 담당할 prod.py 파일
# 보통 운영 환경을 production 환경 (prod.py의 prod는 production의 약어)

ALLOWED_HOSTS = ['15.165.77.106']
STATIC_ROOT = BASE_DIR / 'static/'
# 관리자 앱의 정적 파일을 STATIC_ROOT 디렉터리로 복사
STATICFILES_DIRS = []
# base.py 파일에 STATICFILES_DIRS 항목이 이미 있으니 prod.py 파일에 다시 빈 값으로 설정해서 오류 방지 
# [배포 시작시 명령어] python manage.py runserver --settings=config.settings.prod
