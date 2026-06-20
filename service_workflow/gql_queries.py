import graphene
from graphene_django import DjangoObjectType

from core.gql_queries import InteractiveUserGQLType
from .models import *
from core import prefix_filterset, ExtendedConnection
from location.schema import LocationGQLType
import django_filters
from graphql_relay.node.node import from_global_id


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
        filter_fields = {"id": ["exact"], "type": ["exact", "icontains"]}


class FormSectionGQLType(DjangoObjectType):
    class Meta:
        model = FormSection
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "title": ["exact", "icontains"], "is_active": ["exact"]}


class FormFieldGQLType(DjangoObjectType):
    class Meta:
        model = FormField
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "label": ["exact", "icontains"], "position": ["exact"]}


class FormFieldOptionGQLType(DjangoObjectType):
    class Meta:
        model = FormFieldOption
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "option_value": ["exact", "icontains"]}


class UserFormSubmissionGQLType(DjangoObjectType):
    class Meta:
        model = UserFormSubmission
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "submission_date": ["exact"]}


class UserFormDataGQLType(DjangoObjectType):
    class Meta:
        model = UserFormData
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "value": ["exact", "icontains"]}


class WorkflowStepGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStep
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "step_no": ["exact"], "is_active": ["exact"]}


class WorkflowStepAvailableFieldGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStepAvailableField
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "is_active": ["exact"]}


class WorkflowStepApprovalGQLType(DjangoObjectType):
    class Meta:
        model = WorkflowStepApproval
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "is_approved": ["exact"]}

class SystemUserGQLType(DjangoObjectType):
    class Meta:
        model = InteractiveUser
        interfaces = (graphene.relay.Node,)
        filter_fields = {"id": ["exact"], "login_name": ["exact", "icontains"]}
