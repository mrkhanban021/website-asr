from django.apps import AppConfig


class IdentifyConfig(AppConfig):
    name = 'identify'
    
    def ready(self) -> None:
        import identify.signals
