from .base import *
# 서버 환경을 담당할 prod.py 파일
# 보통 운영 환경을 production 환경 (prod.py의 prod는 production의 약어)

ALLOWED_HOSTS = ['15.165.77.106']

# [배포 시작시 명령어] python manage.py runserver --settings=config.settings.prod
