import logging
import os
import uuid
from core.services import BaseService
from django.db.models import Q
from django.core.files.storage import default_storage
from service_workflow.models import UserFormData

logger = logging.getLogger(__name__)


class UserFormDataServices(BaseService):
    OBJECT_TYPE = UserFormData
    UPLOAD_FOLDER = 'service_workflow/contents/'

    def get(self, **kwargs):
        filters = []
        model = self.OBJECT_TYPE
        client_mutation_id = kwargs.get("client_mutation_id", None)
        if client_mutation_id:
            filters.append(Q(json_ext__contains={"client_mutation_id": client_mutation_id}))
        query = model.objects.filter(*filters, is_deleted=False).all()
        return query

    def create(self, obj_data):
        obj_data["user_created"] = self.user
        obj_data = self._handle_file_upload(obj_data)
        return super().create(obj_data)

    def update(self, obj_data):
        obj_data["user_updated"] = self.user
        obj_data = self._handle_file_upload(obj_data)
        return super().update(obj_data)

    def delete(self, obj_data):
        obj_data["user_updated"] = self.user
        instance = UserFormData.objects.get(id=obj_data["id"])
        # Delete file if it exists
        if instance.file_path:
            try:
                if default_storage.exists(instance.file_path):
                    default_storage.delete(instance.file_path)
            except Exception as e:
                logger.warning(f"Could not delete file {instance.file_path}: {str(e)}")
        instance.delete(username=self.user.username)

    def _handle_file_upload(self, obj_data):
        """Handle file upload for UserFormData"""
        if 'file' in obj_data and obj_data['file']:
            file_obj = obj_data.pop('file')
            try:
                # Generate unique filename
                file_name = f"{uuid.uuid4()}_{file_obj.name}"
                file_path = os.path.join(self.UPLOAD_FOLDER, file_name).replace('\\', '/')
                
                # Save file
                saved_path = default_storage.save(file_path, file_obj)
                
                # Generate file URL
                file_url = default_storage.url(saved_path)
                
                obj_data['file_path'] = saved_path
                obj_data['file_url'] = file_url
            except Exception as e:
                logger.error(f"Error uploading file: {str(e)}")
                raise ValueError(f"File upload failed: {str(e)}")
        
        return obj_data
