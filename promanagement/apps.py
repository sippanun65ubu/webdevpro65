from django.apps import AppConfig


class PromanagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "promanagement"

    def ready(self):
        import promanagement.signals