import logging

from core.services import BaseService
from django.db.models import Q

from service_workflow.models import FormInputType

logger = logging.getLogger(__name__)


class FormInputTypeServices(BaseService):
    OBJECT_TYPE = FormInputType

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
        return super().create(obj_data)

    def update(self, obj_data):
        obj_data["user_updated"] = self.user
        return super().update(obj_data)

    def delete(self, obj_data):
        obj_data["user_updated"] = self.user
        FormInputType.objects.get(id=obj_data["id"]).delete(username=self.user.username)
