import os
import io
import tempfile
import mimetypes
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from AutenticationApp.models import Document,User
from AutenticationApp.serializers import DocumentSerializer
from .permissions import IsAdminOrOwner,IsOwnerOrReadOnly
from docx import Document as DocxDocument
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from .paginations import DocumenttSmallesetPagination







class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DocumenttSmallesetPagination
    filter_backends = [SearchFilter]
    search_fields = ['title','description']

    def get_queryset(self):
        ######
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        description = self.request.query_params.get('description', None)
        ####
        search_query = self.request.query_params.get('search', None)

        if search_query is not None:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(description__icontains=search_query)

        return queryset

    def perform_create(self, serializer):
        file = self.request.data.get('file')
        if file:
            file_format = file.name.split('.')[-1].lower()
            if file_format not in ['pdf', 'docx', 'txt']:
                return Response({'error': 'Invalid file format. Supported formats: pdf, docx, txt.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check file size (example limit: 5 MB)
            max_file_size = 5 * 1024 * 1024
            if file.size > max_file_size:
                return Response({'error': 'File size exceeds the limit (5 MB).'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=self.request.user)



class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]





class DocumentShareView(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def update(self, request, *args, **kwargs):
        document = self.get_object()
        user_ids = request.data.get('shared_with', [])
        shared_with_users = document.shared_with.all()
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            if user != document.owner and user not in shared_with_users:
                document.shared_with.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly])
def convert_document_format(request, document_id, target_format):
    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user == document.owner or request.user.is_staff:
        if target_format not in ['pdf', 'docx', 'txt']:
            return Response({'error': 'Invalid target format'}, status=status.HTTP_400_BAD_REQUEST)

        original_file_path = document.file.path
        output_file_format = target_format.lower()

        if output_file_format == 'pdf':
            if document.format == 'pdf':
                return Response({'error': 'Document already in PDF format'}, status=status.HTTP_400_BAD_REQUEST)

            pdf_output = PdfFileWriter()
            with open(original_file_path, 'rb') as input_file:
                input_pdf = PdfFileReader(input_file)
                for page_num in range(input_pdf.getNumPages()):
                    pdf_output.addPage(input_pdf.getPage(page_num))
            
            output_pdf_path = os.path.join(tempfile.mkdtemp(), f'{document.title}.pdf')
            with open(output_pdf_path, 'wb') as output_file:
                pdf_output.write(output_file)
            
            response = HttpResponse(open(output_pdf_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
            return response

        elif output_file_format == 'docx':
            if document.format == 'docx':
                return Response({'error': 'Document already in DOCX format'}, status=status.HTTP_400_BAD_REQUEST)

            docx = DocxDocument()
            with open(original_file_path, 'rb') as input_file:
                docx.add_paragraph(input_file.read())

            output_docx_path = os.path.join(tempfile.mkdtemp(), f'{document.title}.docx')
            docx.save(output_docx_path)

            response = HttpResponse(open(output_docx_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{document.title}.docx"'
            return response

        elif output_file_format == 'txt':
            if document.format == 'txt':
                return Response({'error': 'Document already in TXT format'}, status=status.HTTP_400_BAD_REQUEST)

            with open(original_file_path, 'r') as input_file:
                text = input_file.read()

            output_txt_path = os.path.join(tempfile.mkdtemp(), f'{document.title}.txt')
            with open(output_txt_path, 'w') as output_file:
                output_file.write(text)

            response = HttpResponse(open(output_txt_path, 'r'), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{document.title}.txt"'
            return response

    else:
        raise PermissionDenied()


