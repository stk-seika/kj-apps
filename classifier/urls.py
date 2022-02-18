from django.urls import path
from django.conf.urls.static import static

from . import views

app_name = 'classifier'

urlpatterns = [
    path('', views.ClassifierView.as_view(), name='classifier'),
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
