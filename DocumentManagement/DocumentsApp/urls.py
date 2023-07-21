
from django.urls import path
from .views import DocumentListCreateView, DocumentDetailView, DocumentShareView, convert_document_format

urlpatterns = [
    path('documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:pk>/share/', DocumentShareView.as_view(), name='document-share'),
    path('documents/<int:document_id>/convert/<str:target_format>/', convert_document_format, name='convert-document-format'),
]

















"""
documents/:
    Maps to the DocumentListCreateView view for listing and creating documents.
documents/<int:pk>/: 
    Maps to the DocumentDetailView view for retrieving, updating, anddeleting a specific document.
documents/<int:pk>/share/: 
    Maps to the DocumentShareView view for sharing a document with other users.
documents/<int:document_id>/convert/<str:target_format>/: 
    Maps to the convert_document_format view for converting a document from one format to another (PDF, DOCX, or TXT).
"""
