from django.urls import path

from .views import (
    AnnotationCreateView,
    AnnotationDetailView,
    AnnotationListView,
    annotation_api_view,
    annotation_qr_download_view,
)

app_name = 'website'

urlpatterns = [
    path('', AnnotationListView.as_view(), name='annotation-list'),
    path('create/', AnnotationCreateView.as_view(), name='annotation-create'),
    path('<uuid:pk>/', AnnotationDetailView.as_view(), name='annotation-detail'),
    path('<uuid:pk>/qr/', annotation_qr_download_view, name='annotation-qr-download'),
    path('api/annotations/<uuid:pk>/', annotation_api_view, name='annotation-api'),
]