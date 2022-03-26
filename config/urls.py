from django.contrib import admin
from django.urls import include, path   # pybo/ URL에 대한 매핑이 path('pybo/', views.index) 에서 path('pybo/', include('pybo.urls'))로 수정
# from pybo import views # 이제 사용하지 않으므로 매핑하지 않음
from pybo.views import base_views

urlpatterns = [ # http://localhost:8000/"app_name"/ 으로 시작하는 URL은 모두 "app_name"/urls.py 파일을 참조
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),
    path('pybo/', include('pybo.urls')),        # pybo app을 사용하기 위해 등록
    path('common/', include('common.urls')),    # common app을 사용하기 위해 등록
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path,  pybo/views.py 파일의 index 함수가 실행
]