from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('image-to-pdf/', views.image_to_pdf, name='image_to_pdf'),
    path('pdf-to-image/', views.pdf_to_image, name='pdf_to_image'),
    path('compress-image/', views.compress_image, name='compress_image'),
      
]
