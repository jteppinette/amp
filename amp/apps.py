from django.apps import AppConfig


class AMPConfig(AppConfig):
    name = "amp"
    verbose_name = "AMP"

    def ready(self):
        from amp import signals  # NOQA
