from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('view/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
    path('results/<int:pdf_id>/', views.ocr_results, name='ocr_results'),
    path('receive_box_images/', views.receive_box_images, name='receive_box_images'),  # Updated endpoint
]
