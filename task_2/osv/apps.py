from django.apps import AppConfig


class OsvConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "osv"
    verbose_name = "Банковские ведомости"

    def ready(self):
        import task_2.signals
