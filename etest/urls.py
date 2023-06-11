
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register/', resgister, name='resgister'),
    path('test/', test, name='test'),
    path('logout', logout_button, name='logout'),
    path('audio-file', audio_file, name='audio_file'),
    path('get-certificate/<str:level>', generate_certificate, name='generate_certificate'),
    path('result/<str:token>', result_page, name='result_page'),
    path('question-generator', question_generator, name='question_generator'),
]
urlpatterns = urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)