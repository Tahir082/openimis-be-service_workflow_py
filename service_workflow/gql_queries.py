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
        import graphene
        import graphene_django_optimizer as gql_optimizer
        from graphene_django import DjangoObjectType

        from core.schema import OrderedDjangoFilterConnectionField
        from .models import *
        from .gql_types import *
        from .services.public_service_services import PublicServiceServices
        from .services.form_input_type_services import FormInputTypeServices
        from .services.form_section_services import FormSectionServices
        from .services.form_field_services import FormFieldServices
        from .services.form_field_option_services import FormFieldOptionServices
        from .services.user_form_submission_services import UserFormSubmissionServices
        from .services.user_form_data_services import UserFormDataServices
        from .services.workflow_step_services import WorkflowStepServices
        from .services.workflow_step_available_field_services import WorkflowStepAvailableFieldServices
        from .services.workflow_step_approval_services import WorkflowStepApprovalServices


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
