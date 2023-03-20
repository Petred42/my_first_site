from django.apps import AppConfig


class FirstAttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'first_att'

    def ready(self):
        import first_att.signals
