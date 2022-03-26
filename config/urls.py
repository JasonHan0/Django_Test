from django.contrib import admin
# pybo/ URL에 대한 매핑이 path('pybo/', views.index) 에서 path('pybo/', include('pybo.urls'))로 수정
from django.urls import include, path
# from pybo import views # 위의 inclue를 추가함으로 view를 불러오지 않아도 됨

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    # path('pybo/', views.index),
]
