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
from .services.public_service_services import PublicServiceServices
from .services.form_input_type_services import FormInputTypeServices
from .services.form_section_services import FormSectionServices
from .services.form_field_services import FormFieldServices
from .services.form_field_option_services import FormFieldOptionServices
from .services.user_form_submission_services import UserFormSubmissionServices
from .services.user_form_data_services import UserFormDataServices
from .services.visitor_user_services import VisitorUserServices
from .services.workflow_step_services import WorkflowStepServices
from .services.workflow_step_available_field_services import WorkflowStepAvailableFieldServices
from .services.workflow_step_approval_services import WorkflowStepApprovalServices
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


class CreateVisitorUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        otp = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import VisitorUser
        try:
            VisitorUser.objects.create(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])

class UpdateVisitorUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        otp = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import VisitorUser
        try:
            # VisitorUser.objects.update(**data)
            obj= VisitorUser.objects.get(id=data["id"])
            obj.name = data["name"]
            obj.email = data["email"]
            obj.otp= data["otp"]
            obj.save();
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])

class DeleteVisitorUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        otp = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import VisitorUser
        try:
            visitor_user= VisitorUser.objects.get(id=data["id"])
            visitor_user.delete()
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])

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

class DeletePublicServiceMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeletePublicServiceMutation"

    class Input(PublicServiceInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_public_service"
        service_instance = PublicServiceServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data
        )
        return result


class CreateFormInputTypeMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateFormInputTypeMutation"

    class Input(FormInputTypeInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_form_input_type"
        service_instance = FormInputTypeServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateFormInputTypeMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateFormInputTypeMutation"

    class Input(FormInputTypeInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_form_input_type"
        service_instance = FormInputTypeServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteFormInputTypeMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteFormInputTypeMutation"

    class Input(FormInputTypeInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_form_input_type"
        service_instance = FormInputTypeServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateFormSectionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateFormSectionMutation"

    class Input(FormSectionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_form_section"
        service_instance = FormSectionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateFormSectionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateFormSectionMutation"

    class Input(FormSectionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_form_section"
        service_instance = FormSectionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteFormSectionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteFormSectionMutation"

    class Input(FormSectionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_form_section"
        service_instance = FormSectionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateFormFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateFormFieldMutation"

    class Input(FormFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_form_field"
        service_instance = FormFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateFormFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateFormFieldMutation"

    class Input(FormFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_form_field"
        service_instance = FormFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteFormFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteFormFieldMutation"

    class Input(FormFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_form_field"
        service_instance = FormFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateFormFieldOptionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateFormFieldOptionMutation"

    class Input(FormFieldOptionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_form_field_option"
        service_instance = FormFieldOptionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateFormFieldOptionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateFormFieldOptionMutation"

    class Input(FormFieldOptionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_form_field_option"
        service_instance = FormFieldOptionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteFormFieldOptionMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteFormFieldOptionMutation"

    class Input(FormFieldOptionInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_form_field_option"
        service_instance = FormFieldOptionServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateUserFormSubmissionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        public_service_id = graphene.String()
        submission_date = graphene.Date()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormSubmission
        try:
            UserFormSubmission.objects.create(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class UpdateUserFormSubmissionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        public_service_id = graphene.String()
        submission_date = graphene.Date()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormSubmission
        try:
            UserFormSubmission.objects.update(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class DeleteUserFormSubmissionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        public_service_id = graphene.String()
        submission_date = graphene.Date()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormSubmission
        try:
            obj = UserFormSubmission.objects.get(id=data["id"])
            obj.delete()
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class CreateUserFormDataMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        user_form_submission_id = graphene.String()
        public_service_id = graphene.String()
        form_section_id = graphene.String()
        form_field_id = graphene.String()
        form_field_option_id = graphene.String()
        value = graphene.String()
        file = graphene.String()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormData
        try:
            UserFormData.objects.create(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class UpdateUserFormDataMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        user_form_submission_id = graphene.String()
        public_service_id = graphene.String()
        form_section_id = graphene.String()
        form_field_id = graphene.String()
        form_field_option_id = graphene.String()
        value = graphene.String()
        file = graphene.String()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormData
        try:
            UserFormData.objects.update(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class DeleteUserFormDataMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        user_form_submission_id = graphene.String()
        public_service_id = graphene.String()
        form_section_id = graphene.String()
        form_field_id = graphene.String()
        form_field_option_id = graphene.String()
        value = graphene.String()
        file = graphene.String()
        visitor_user_id = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import UserFormData
        try:
            obj = UserFormData.objects.get(id=data["id"])
            obj.delete()
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class CreateWorkflowStepMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateWorkflowStepMutation"

    class Input(WorkflowStepInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_workflow_step"
        service_instance = WorkflowStepServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateWorkflowStepMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateWorkflowStepMutation"

    class Input(WorkflowStepInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_workflow_step"
        service_instance = WorkflowStepServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteWorkflowStepMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteWorkflowStepMutation"

    class Input(WorkflowStepInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_workflow_step"
        service_instance = WorkflowStepServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateWorkflowStepAvailableFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateWorkflowStepAvailableFieldMutation"

    class Input(WorkflowStepAvailableFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_workflow_step_available_field"
        service_instance = WorkflowStepAvailableFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class UpdateWorkflowStepAvailableFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateWorkflowStepAvailableFieldMutation"

    class Input(WorkflowStepAvailableFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_workflow_step_available_field"
        service_instance = WorkflowStepAvailableFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteWorkflowStepAvailableFieldMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteWorkflowStepAvailableFieldMutation"

    class Input(WorkflowStepAvailableFieldInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_workflow_step_available_field"
        service_instance = WorkflowStepAvailableFieldServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class CreateWorkflowStepApprovalMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "CreateWorkflowStepApprovalMutation"

    class Input(WorkflowStepApprovalInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_create_workflow_step_approval"
        service_instance = WorkflowStepApprovalServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='create',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result
    
class CreateWorkflowStepApprovalPublicMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        user_form_submission_id = graphene.String()
        workflow_step_id = graphene.String()
        remarks = graphene.String()
        from_user_id = graphene.String()
        to_user_id = graphene.String()
        is_approved = graphene.Boolean()
        is_reverted = graphene.Boolean()
        final_approved = graphene.Boolean()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **data):
        from .models import WorkflowStepApproval
        try:
            WorkflowStepApproval.objects.create(**data)
            return cls(success=True, errors=[])
        except Exception as e:
            return cls(success=False, errors=[str(e)])


class UpdateWorkflowStepApprovalMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "UpdateWorkflowStepApprovalMutation"

    class Input(WorkflowStepApprovalInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_update_workflow_step_approval"
        service_instance = WorkflowStepApprovalServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='update',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result


class DeleteWorkflowStepApprovalMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_module = mutation_module
    _mutation_class = "DeleteWorkflowStepApprovalMutation"

    class Input(WorkflowStepApprovalInputType):
        pass

    @classmethod
    def _mutate(cls, user, **data):
        failure_message = "service_workflow.mutation.failed_to_delete_workflow_step_approval"
        service_instance = WorkflowStepApprovalServices(user)
        result = auth_permission_validation(
            failure_message=failure_message,
            call_type='delete',
            service_instance=service_instance,
            user=user,
            data=data,
        )
        return result