from operator import truediv

from django.db import models
from core.models import HistoryModel, InteractiveUser
from core.models.user import Role
from core.models.user import RoleRight
from location.models import Location
from django.utils import timezone
from datetime import timedelta
import secrets
import uuid
from datetime import datetime as py_datetime

class PublicService(HistoryModel):
    title = models.TextField(
        blank=True,
        null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'sw_public_services'


class FormInputType(HistoryModel):
    type = models.CharField(
        max_length=50,
        blank=True,
        null=False)

    class Meta:
        managed = True
        db_table = 'sw_form_input_types'

class FormSection(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_section_public_service",
    )
    title = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    step_no = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = 'sw_form_sections'

class FormField(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_field_public_service",
    )
    form_section= models.ForeignKey(
        "FormSection",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_field_form_section"
    )
    form_input_type= models.ForeignKey(
        "FormInputType",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_field_form_input_type"
    )
    label = models.TextField(blank=True,null=True)
    placeholder = models.TextField(blank=True,null=True)
    default_value = models.TextField(blank=True,null=True)
    is_required = models.BooleanField(blank=True,null=True)
    min_value = models.TextField(blank=True,null=True)
    max_value = models.TextField(blank=True,null=True)
    value_step = models.FloatField(blank=True,null=True)
    position = models.IntegerField(blank=True,null=True,default=0)
    is_multiselect = models.BooleanField(blank=True,null=True)
    help_text = models.TextField(blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'sw_form_fields'


class FormFieldOption(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_field_option_public_service",
    )
    form_field= models.ForeignKey(
        "FormField",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="form_field_option_form_field"
    )
    option_value = models.TextField(blank=True,null=True)
    option_text = models.TextField(blank=True,null=True)
    is_preselected = models.BooleanField(blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'sw_form_field_options'



class UserFormSubmission(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_submission_public_service",
    )
    submission_date = models.DateField(blank=True,null=True)
    interactive_user= models.ForeignKey(
        InteractiveUser,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_submission_interactive_user",
    )
    class Meta:
        managed = True
        db_table = 'sw_user_form_submissions'


class UserFormData(HistoryModel):
    user_form_submission= models.ForeignKey(
        "UserFormSubmission",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_submission",
    )
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_public_service",
    )
    form_section = models.ForeignKey(
        "FormSection",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_form_section"
    )
    form_field= models.ForeignKey(
        "FormField",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_form_field"
    )
    form_field_option= models.ForeignKey(
        "FormFieldOption",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_form_field_option"
    )
    value = models.TextField(blank=True,null=True)
    file_url= models.TextField(blank=True,null=True)
    file_path= models.TextField(blank=True,null=True)
    interactive_user= models.ForeignKey(
        InteractiveUser,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="user_form_data_interactive_user",
    )
    class Meta:
        managed = True
        db_table = 'sw_user_form_data'


class WorkflowStep(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_public_service",
    )
    interactive_user= models.ForeignKey(
        InteractiveUser,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_interactive_user",
    )
    step_no = models.IntegerField(blank=True,null=True)
    workflow_role = models.TextField(blank=True,null=True)
    responsibility = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'sw_workflow_steps'

class WorkflowStepAvailableField(HistoryModel):
    public_service = models.ForeignKey(
        "PublicService",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_available_field_public_service",
    )
    form_field= models.ForeignKey(
        "FormField",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_available_field_form_field",
    )
    workflow_step= models.ForeignKey(
        "WorkflowStep",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_available_field_workflow_step",
    )
    is_active = models.BooleanField(blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'sw_workflow_step_available_fields'


class WorkflowStepApproval(HistoryModel):
    user_form_submission= models.ForeignKey(
        "UserFormSubmission",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_approval_user_form_submission",
    )
    workflow_step= models.ForeignKey(
        "WorkflowStep",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_approval_workflow_step",
    )
    remarks = models.TextField(blank=True,null=True)
    from_user = models.ForeignKey(
        InteractiveUser,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_approval_from_user",
    )
    to_user = models.ForeignKey(
        InteractiveUser,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="workflow_step_approval_to_user",
    )
    is_approved= models.BooleanField(blank=True,null=True)
    is_reverted= models.BooleanField(blank=True,null=True)


    class Meta:
        managed = True
        db_table = 'sw_workflow_step_approvals'

