import graphene
from graphene_django import DjangoObjectType
import django_filters
from graphql_relay.node.node import from_global_id

from core.gql_queries import InteractiveUserGQLType
from .models import *
from core import prefix_filterset, ExtendedConnection
from location.schema import LocationGQLType


class VisitorUserGQLType(DjangoObjectType):
    class Meta:
        model = VisitorUser
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "email": ["exact", "icontains"],
            "otp": ["exact"],
        }

class PublicServiceGQLType(DjangoObjectType):
    class Meta:
        model = PublicService
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "title": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "is_active": ["exact"],
        }


class FormInputTypeGQLType(DjangoObjectType):
    class Meta:
        model = FormInputType
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "type": ["exact", "icontains"]
        }


class FormSectionGQLType(DjangoObjectType):
    class Meta:
        model = FormSection
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "title": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "step_no": ["exact", "gt", "lt", "gte", "lte"],
            "is_active": ["exact"]
        }


class FormFieldGQLType(DjangoObjectType):
    class Meta:
        model = FormField
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "form_section": ["exact"],
            "form_input_type": ["exact"],
            "label": ["exact", "icontains"],
            "placeholder": ["exact", "icontains"],
            "default_value": ["exact", "icontains"],
            "is_required": ["exact"],
            "min_value": ["exact", "icontains"],
            "max_value": ["exact", "icontains"],
            "value_step": ["exact", "gt", "lt", "gte", "lte"],
            "position": ["exact", "gt", "lt", "gte", "lte"],
            "is_multiselect": ["exact"],
            "help_text": ["exact", "icontains"],
        }


class FormFieldOptionGQLType(DjangoObjectType):
    class Meta:
        model = FormFieldOption
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "form_field": ["exact"],
            "option_value": ["exact", "icontains"],
            "option_text": ["exact", "icontains"],
            "is_preselected": ["exact"]
        }


class UserFormSubmissionGQLType(DjangoObjectType):
    class Meta:
        model = UserFormSubmission
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "submission_date": ["exact", "gt", "lt", "gte", "lte"],
            "visitor_user": ["exact"]
        }


class UserFormDataGQLType(DjangoObjectType):
    class Meta:
        model = UserFormData
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "user_form_submission": ["exact"],
            "public_service": ["exact"],
            "form_section": ["exact"],
            "form_field": ["exact"],
            "form_field_option": ["exact"],
            "value": ["exact", "icontains"],
            "file_url": ["exact", "icontains"],
            "file_path": ["exact", "icontains"],
            "visitor_user": ["exact"]
        }


class WorkflowStepGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStep
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "interactive_user": ["exact"],
            "step_no": ["exact", "gt", "lt", "gte", "lte"],
            "workflow_role": ["exact", "icontains"],
            "responsibility": ["exact", "icontains"],
            "is_active": ["exact"]
        }


class WorkflowStepAvailableFieldGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStepAvailableField
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "public_service": ["exact"],
            "form_field": ["exact"],
            "workflow_step": ["exact"],
            "is_active": ["exact"]
        }


class WorkflowStepApprovalGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStepApproval
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "user_form_submission": ["exact"],
            "workflow_step": ["exact"],
            "remarks": ["exact", "icontains"],
            "from_user": ["exact"],
            "to_user": ["exact"],
            "is_approved": ["exact"],
            "is_reverted": ["exact"],
            "final_approved": ["exact"],
            "is_sent": ["exact"]
        }


class SystemUserGQLType(DjangoObjectType):
    class Meta:
        model = InteractiveUser
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "login_name": ["exact", "icontains"]
        }