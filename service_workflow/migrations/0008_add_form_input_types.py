# Generated data migration for FormInputType seed data

from django.db import migrations
import uuid


def create_form_input_types(apps, schema_editor):
    FormInputType = apps.get_model('service_workflow', 'FormInputType')
    user_id = uuid.UUID('da34a889-deba-4857-8dee-9ba4e38e80bb')
    

    data =[
        {
            "id": uuid.uuid4(),
            "type": "text",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "select",
            "user_created_id": user_id,
            "user_updated_id": user_id,

        },
        {
            "id": uuid.uuid4(),
            "type": "select2",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "multiselect",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "radio",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "checkbox",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "url",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "email",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "password",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "file",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
        {
            "id": uuid.uuid4(),
            "type": "textarea",
            "user_created_id": user_id,
            "user_updated_id": user_id,
        },
    ]
    
    for item in data:
        FormInputType.objects.create(**item)


def reverse_form_input_types(apps, schema_editor):
    FormInputType = apps.get_model('service_workflow', 'FormInputType')
    FormInputType.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('service_workflow', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_form_input_types, reverse_form_input_types),
    ]
