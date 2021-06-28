from django.urls import path
from .views import MainpageView, DownloadpageView
from . import views

urlpatterns = [
    path('', MainpageView.as_view(), name='home'),
    path('download/', DownloadpageView.as_view(), name='download'),
    #path('<str:filepath>/', views.download),
]

#handler404 = 'filecryptography.views.handler404'
#handler500 = 'filecryptography.views.handler500'
