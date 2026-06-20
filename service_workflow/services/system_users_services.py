import logging

from core.models import InteractiveUser
from core.services import BaseService
from django.db.models import Q

from service_workflow.models import WorkflowStepApproval

logger = logging.getLogger(__name__)


class SystemUsersServices(BaseService):
    OBJECT_TYPE = InteractiveUser

    def get(self, **kwargs):
        filters = []
        model = self.OBJECT_TYPE
        client_mutation_id = kwargs.get("client_mutation_id", None)
        if client_mutation_id:
            filters.append(Q(json_ext__contains={"client_mutation_id": client_mutation_id}))
        query = model.objects.filter(*filters).all()
        if "id" in kwargs:
            query = query.filter(id=kwargs["id"])
        if "login_name" in kwargs:
            query = query.filter(login_name=kwargs["login_name"])
        return query

    def create(self, obj_data):
        obj_data["user_created"] = self.user
        return super().create(obj_data)

    def update(self, obj_data):
        obj_data["user_updated"] = self.user
        return super().update(obj_data)

