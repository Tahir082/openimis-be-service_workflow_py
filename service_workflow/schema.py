import os
from collections import defaultdict

import graphene
import graphene_django_optimizer as gql_optimizer
import requests
from django.db.models import Count
from django.db.models import F
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext as _
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from core.models.user import InteractiveUser
from core.models.user import UserRole
from core.schema import OrderedDjangoFilterConnectionField
from .gql_mutations import *
from .gql_queries import *
from .models import *
from .services.public_service_services import PublicServiceServices
from .services.system_users_services import SystemUsersServices
from django.db.models.expressions import RawSQL


class Query(graphene.ObjectType):
    public_service = OrderedDjangoFilterConnectionField(
        PublicServiceGQLType, client_mutation_id=graphene.String(), orderBy=graphene.List(of_type=graphene.String)
    )
    form_input_type = OrderedDjangoFilterConnectionField(FormInputTypeGQLType, client_mutation_id=graphene.String())
    form_section = OrderedDjangoFilterConnectionField(FormSectionGQLType, client_mutation_id=graphene.String())
    form_field = OrderedDjangoFilterConnectionField(FormFieldGQLType, client_mutation_id=graphene.String())
    form_field_option = OrderedDjangoFilterConnectionField(FormFieldOptionGQLType, client_mutation_id=graphene.String())
    user_form_submission = OrderedDjangoFilterConnectionField(UserFormSubmissionGQLType,
                                                              client_mutation_id=graphene.String())
    user_form_data = OrderedDjangoFilterConnectionField(UserFormDataGQLType, client_mutation_id=graphene.String())
    workflow_step = OrderedDjangoFilterConnectionField(WorkflowStepGQLType, client_mutation_id=graphene.String())
    workflow_step_available_field = OrderedDjangoFilterConnectionField(WorkflowStepAvailableFieldGQLType,
                                                                       client_mutation_id=graphene.String())
    workflow_step_approval = OrderedDjangoFilterConnectionField(WorkflowStepApprovalGQLType,
                                                                client_mutation_id=graphene.String())
    system_users= graphene.List(SystemUserGQLType,
                                client_mutation_id=graphene.String())

    def resolve_public_service(self, info, **kwargs):
        service = PublicServiceServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_form_input_type(self, info, **kwargs):
        service = FormInputTypeServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_form_section(self, info, **kwargs):
        service = FormSectionServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_form_field(self, info, **kwargs):
        service = FormFieldServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_form_field_option(self, info, **kwargs):
        service = FormFieldOptionServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_user_form_submission(self, info, **kwargs):
        service = UserFormSubmissionServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_user_form_data(self, info, **kwargs):
        service = UserFormDataServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_workflow_step(self, info, **kwargs):
        service = WorkflowStepServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_workflow_step_available_field(self, info, **kwargs):
        service = WorkflowStepAvailableFieldServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_workflow_step_approval(self, info, **kwargs):
        service = WorkflowStepApprovalServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)

    def resolve_system_users(self, info, **kwargs):
        service = SystemUsersServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)


class Mutation(graphene.ObjectType):
    create_public_service = CreatePublicServiceMutation.Field()
    update_public_service = UpdatePublicServiceMutation.Field()
    delete_public_service = DeletePublicServiceMutation.Field()

    create_form_input_type = CreateFormInputTypeMutation.Field()
    update_form_input_type = UpdateFormInputTypeMutation.Field()
    delete_form_input_type = DeleteFormInputTypeMutation.Field()

    create_form_section = CreateFormSectionMutation.Field()
    update_form_section = UpdateFormSectionMutation.Field()
    delete_form_section = DeleteFormSectionMutation.Field()

    create_form_field = CreateFormFieldMutation.Field()
    update_form_field = UpdateFormFieldMutation.Field()
    delete_form_field = DeleteFormFieldMutation.Field()

    create_form_field_option = CreateFormFieldOptionMutation.Field()
    update_form_field_option = UpdateFormFieldOptionMutation.Field()
    delete_form_field_option = DeleteFormFieldOptionMutation.Field()

    create_user_form_submission = CreateUserFormSubmissionMutation.Field()
    update_user_form_submission = UpdateUserFormSubmissionMutation.Field()
    delete_user_form_submission = DeleteUserFormSubmissionMutation.Field()

    create_user_form_data = CreateUserFormDataMutation.Field()
    update_user_form_data = UpdateUserFormDataMutation.Field()
    delete_user_form_data = DeleteUserFormDataMutation.Field()

    create_workflow_step = CreateWorkflowStepMutation.Field()
    update_workflow_step = UpdateWorkflowStepMutation.Field()
    delete_workflow_step = DeleteWorkflowStepMutation.Field()

    create_workflow_step_available_field = CreateWorkflowStepAvailableFieldMutation.Field()
    update_workflow_step_available_field = UpdateWorkflowStepAvailableFieldMutation.Field()
    delete_workflow_step_available_field = DeleteWorkflowStepAvailableFieldMutation.Field()

    create_workflow_step_approval = CreateWorkflowStepApprovalMutation.Field()
    update_workflow_step_approval = UpdateWorkflowStepApprovalMutation.Field()
    delete_workflow_step_approval = DeleteWorkflowStepApprovalMutation.Field()