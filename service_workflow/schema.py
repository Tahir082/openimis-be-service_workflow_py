import os
from collections import defaultdict
from os import name

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

from .services.visitor_user_services import VisitorUserServices


class Query(graphene.ObjectType):
    visitor_user = graphene.List(
        VisitorUserGQLType,
        id= graphene.String(),
        name= graphene.String(),
        email= graphene.String(),
        otp= graphene.String()
    )
    public_public_service = graphene.List(
        PublicServiceGQLType,
        id= graphene.String(),
        title= graphene.String(),
        description= graphene.String(),
        is_active= graphene.Boolean()
    )
    public_form_input_type = graphene.List(
        FormInputTypeGQLType,
        id= graphene.String(),
        type_name= graphene.String()
    )
    public_form_section = graphene.List(
        FormSectionGQLType,
        id= graphene.String(),
        public_service_id= graphene.String(),
        title= graphene.String(),
        description= graphene.String(),
        step_no= graphene.Int(),
        is_active= graphene.Boolean()
    )
    public_form_field = graphene.List(
        FormFieldGQLType,
        id= graphene.String(),
        public_service_id= graphene.String(),
        form_section_id= graphene.String(),
        form_input_type_id= graphene.String(),
        label= graphene.String(),
        is_required= graphene.Boolean(),
        is_multiselect= graphene.Boolean()
    )
    public_form_field_option = graphene.List(
        FormFieldOptionGQLType,
        id= graphene.String(),
        public_service_id= graphene.String(),
        form_field_id= graphene.String(),
        option_value= graphene.String(),
        option_text= graphene.String(),
        is_preselected= graphene.Boolean()
    )
    public_user_form_submission = graphene.List(
        UserFormSubmissionGQLType,
        id= graphene.String(),
        public_service_id= graphene.String(),
        visitor_user_id= graphene.String()
    )
    public_user_form_data = graphene.List(
        UserFormDataGQLType,
        id= graphene.String(),
        user_form_submission_id= graphene.String(),
        public_service_id= graphene.String(),
        form_section_id= graphene.String(),
        form_field_id= graphene.String(),
        form_field_option_id= graphene.String(),
        visitor_user_id= graphene.String()
    )
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
                                id= graphene.Int(),
                                login_name= graphene.String(),
                                client_mutation_id=graphene.String())

    def resolve_visitor_user(self, info, id=None, name=None, email=None, otp=None):
        qs= VisitorUser.objects.filter(is_deleted=False)
        if id:
            qs= qs.filter(id=id)
        if name:
            qs.filter(name=name)
        if email:
            qs.filter(email=email)
        if otp:
            qs.filter(otp=otp)
        return qs

    def resolve_public_public_service(self, info, id=None, title=None, description=None, is_active=None):
        qs = PublicService.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if title:
            qs = qs.filter(title__icontains=title)
        if description:
            qs = qs.filter(description__icontains=description)
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
        return qs

    def resolve_public_form_input_type(self, info, id=None, type_name=None):
        qs = FormInputType.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if type_name:
            qs = qs.filter(type__icontains=type_name)
        return qs

    def resolve_public_form_section(self, info, id=None, public_service_id=None, title=None, description=None, step_no=None, is_active=None):
        qs = FormSection.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if public_service_id:
            qs = qs.filter(public_service_id=public_service_id)
        if title:
            qs = qs.filter(title__icontains=title)
        if description:
            qs = qs.filter(description__icontains=description)
        if step_no is not None:
            qs = qs.filter(step_no=step_no)
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
        return qs

    def resolve_public_form_field(self, info, id=None, public_service_id=None, form_section_id=None, form_input_type_id=None, label=None, is_required=None, is_multiselect=None):
        qs = FormField.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if public_service_id:
            qs = qs.filter(public_service_id=public_service_id)
        if form_section_id:
            qs = qs.filter(form_section_id=form_section_id)
        if form_input_type_id:
            qs = qs.filter(form_input_type_id=form_input_type_id)
        if label:
            qs = qs.filter(label__icontains=label)
        if is_required is not None:
            qs = qs.filter(is_required=is_required)
        if is_multiselect is not None:
            qs = qs.filter(is_multiselect=is_multiselect)
        return qs

    def resolve_public_form_field_option(self, info, id=None, public_service_id=None, form_field_id=None, option_value=None, option_text=None, is_preselected=None):
        qs = FormFieldOption.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if public_service_id:
            qs = qs.filter(public_service_id=public_service_id)
        if form_field_id:
            qs = qs.filter(form_field_id=form_field_id)
        if option_value:
            qs = qs.filter(option_value__icontains=option_value)
        if option_text:
            qs = qs.filter(option_text__icontains=option_text)
        if is_preselected is not None:
            qs = qs.filter(is_preselected=is_preselected)
        return qs

    def resolve_public_user_form_submission(self, info, id=None, public_service_id=None, visitor_user_id=None):
        qs = UserFormSubmission.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if public_service_id:
            qs = qs.filter(public_service_id=public_service_id)
        if visitor_user_id:
            qs = qs.filter(visitor_user_id=visitor_user_id)
        return qs

    def resolve_public_user_form_data(self, info, id=None, user_form_submission_id=None, public_service_id=None, form_section_id=None, form_field_id=None, form_field_option_id=None, visitor_user_id=None):
        qs = UserFormData.objects.filter(is_deleted=False)
        if id:
            qs = qs.filter(id=id)
        if user_form_submission_id:
            qs = qs.filter(user_form_submission_id=user_form_submission_id)
        if public_service_id:
            qs = qs.filter(public_service_id=public_service_id)
        if form_section_id:
            qs = qs.filter(form_section_id=form_section_id)
        if form_field_id:
            qs = qs.filter(form_field_id=form_field_id)
        if form_field_option_id:
            qs = qs.filter(form_field_option_id=form_field_option_id)
        if visitor_user_id:
            qs = qs.filter(visitor_user_id=visitor_user_id)
        return qs

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
    create_visitor_user = CreateVisitorUserMutation.Field()
    update_visitor_user = UpdateVisitorUserMutation.Field()
    delete_visitor_user = DeleteVisitorUserMutation.Field()

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