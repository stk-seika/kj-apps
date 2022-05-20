from django.urls import path
from django.conf.urls.static import static

from . import views

app_name = 'th_pixiv_network'

urlpatterns = [
    path('', views.NetworkView.as_view(), name='th_pixiv_network'),
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
