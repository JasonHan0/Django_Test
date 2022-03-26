from .base_views import *
from .question_views import *
from .answer_views import *
from .comment_views import *

# views 디렉터리의 __init__.py 파일에서 views 디렉터리에 있는 base_views.py 등의 모든 뷰 파일의 함수를 import 했기 때문에 
# pybo/urls.py와 같은 다른 모듈에서 views 모듈의 함수를 사용하는 부분을 수정할 필요가 없다.
