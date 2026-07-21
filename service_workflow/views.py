import json
from typing import List

from django.http import Http404, FileResponse
from location.models import Location
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .services.file_services import save_uploaded_file, retrieve_file_response
from core.models import InteractiveUser
import os
from rest_framework.permissions import AllowAny
from django.db.models import F, Sum
from django.db.models.fields.json import KeyTextTransform
from datetime import datetime, timezone, date
import json
import base64

def extract_uuid(encoded_str):
    decoded = base64.b64decode(encoded_str).decode()
    return decoded.split(":")[1]

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        file = request.FILES.get('file')
        name = request.POST.get('name')
        file_url, file_path, error = save_uploaded_file(file, name)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'file_url': file_url, 'file_path': file_path, 'file_name':name}, status=status.HTTP_201_CREATED)


class FileRetrieveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, filename):
        try:
            return retrieve_file_response(filename)
        except Http404 as e:
            raise e
