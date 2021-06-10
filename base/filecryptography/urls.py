from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import MainpageView, DownloadpageView

urlpatterns = [
    path('', MainpageView.as_view(), name='home'),
    path('download/', DownloadpageView.as_view(), name='download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
