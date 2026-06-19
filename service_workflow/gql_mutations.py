from core.gql.gql_mutations.base_mutation import BaseMutation, BaseHistoryModelCreateMutationMixin
from graphql_jwt.mutations import JSONWebTokenMutation, mixins
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
import base64
from core.models import InteractiveUser
from core.schema import OpenIMISMutation
from .apps import ServiceWorkflowConfig
from datetime import date, datetime
import json
import graphene
from .gql_types import *
from .models import *
from .services.public_service_services import PublicServiceServices
from .gql_queries import *
mutation_module = "service_workflow"


def auth_permission_validation(failure_message, call_type, service_instance, user, data):
    """
    Validates user authentication and permissions, processes data, and calls the service method.

    :param failure_message: Error message to return on failure.
    :param required_permission: Permissions required for the action.
    :param call_type: Type of function to call.
    :param service_instance: Instance of the service to call.
    :param user: User performing the action.
    :param data: Data to process.
    :return: None or an error dictionary.
    """
    try:
        if isinstance(user, AnonymousUser) or not user.id:
            raise ValidationError(_("mutation.authentication_required"))

        processed_data = {k: v for k, v in data.items() if k not in [
            "client_mutation_id", "client_mutation_label"]}
        if data.get('client_mutation_id') and data.get('client_mutation_id') != '':
            processed_data['json_ext'] = {
                'client_mutation_id': data.get('client_mutation_id')}

        if call_type == 'create':
            return service_instance.create(processed_data)
        if call_type == 'update':
            return service_instance.update(processed_data)
        if call_type == 'update_status':
            return service_instance.update_status(processed_data)
        if call_type == 'approve':
            return service_instance.approve(processed_data)
        return None
    except Exception as exc:
        return [{
            'message': _(failure_message),
            'detail': str(exc)
        }]


def no_auth_validation(failure_message, call_type, service_instance, data):
    try:
        processed_data = {k: v for k, v in data.items() if k not in [
            "client_mutation_id", "client_mutation_label"]}
        if data.get('client_mutation_id') and data.get('client_mutation_id') != '':
            processed_data['json_ext'] = {
                'client_mutation_id': data.get('client_mutation_id')}
        if call_type == 'create':
            return service_instance.create(processed_data)
        if call_type == 'update':
            return service_instance.update(processed_data)
        if call_type == 'update_status':
            return service_instance.update_status(processed_data)
        return None
    except Exception as exc:
        return [{
            'message': _(failure_message),
            'detail': str(exc)
        }]


class CreatePublicServiceMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreatePublicServiceMutation"

    class Input(PublicServiceInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_public_service"
        service_instance = PublicServiceServices(user)

        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data
        )
        return result

class UpdatePublicServiceMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdatePublicServiceMutation"

    class Input(PublicServiceInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_public_service"
        service_instance = PublicServiceServices(user)

        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data
        )
        return result