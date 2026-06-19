import graphene

from core.schema import OpenIMISMutation


class PublicServiceInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    title = graphene.String(required=False)
    description = graphene.String(required=False)
    is_active = graphene.Boolean(required=False)


class FormInputTypeInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    type = graphene.String(required=False)


class FormSectionInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    title = graphene.String(required=False)
    description = graphene.String(required=False)
    step_no = graphene.Int(required=False)
    is_active = graphene.Boolean(required=False)


class FormFieldInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    form_section_id = graphene.String(required=False)
    form_input_type_id = graphene.String(required=False)
    label = graphene.String(required=False)
    placeholder = graphene.String(required=False)
    default_value = graphene.String(required=False)
    is_required = graphene.Boolean(required=False)
    min_value = graphene.String(required=False)
    max_value = graphene.String(required=False)
    value_step = graphene.Float(required=False)
    position = graphene.Int(required=False)
    is_multiselect = graphene.Boolean(required=False)
    help_text = graphene.String(required=False)


class FormFieldOptionInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    form_field_id = graphene.String(required=False)
    option_value = graphene.String(required=False)
    option_text = graphene.String(required=False)
    is_preselected = graphene.Boolean(required=False)


class UserFormSubmissionInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    submission_date = graphene.Date(required=False)
    interactive_user_id = graphene.String(required=False)


class UserFormDataInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    user_form_submission_id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    form_section_id = graphene.String(required=False)
    form_field_id = graphene.String(required=False)
    form_field_option_id = graphene.String(required=False)
    value = graphene.String(required=False)
    file = graphene.String(required=False)
    interactive_user_id = graphene.String(required=False)


class WorkflowStepInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    interactive_user_id = graphene.String(required=False)
    step_no = graphene.Int(required=False)
    workflow_role = graphene.String(required=False)
    responsibility = graphene.String(required=False)
    is_active = graphene.Boolean(required=False)


class WorkflowStepAvailableFieldInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    public_service_id = graphene.String(required=False)
    form_field_id = graphene.String(required=False)
    is_active = graphene.Boolean(required=False)


class WorkflowStepApprovalInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    user_form_submission_id = graphene.String(required=False)
    workflow_step_id = graphene.String(required=False)
    remarks = graphene.String(required=False)
    from_user_id = graphene.String(required=False)
    to_user_id = graphene.String(required=False)
    is_approved = graphene.Boolean(required=False)
    is_reverted = graphene.Boolean(required=False)
