from django.apps import AppConfig


class OutboxHitcountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'outbox_hitcount'
