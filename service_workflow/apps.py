from django.apps import AppConfig

MODULE_NAME = 'service_workflow'
DEFAULT_CFG = {}


class ServiceWorkflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = MODULE_NAME

    def ready(self):
        from core.models import ModuleConfiguration

        ModuleConfiguration.get_or_default(self.name, DEFAULT_CFG)
