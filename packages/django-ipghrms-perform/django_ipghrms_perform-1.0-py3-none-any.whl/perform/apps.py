from django.apps import AppConfig


class PerformConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'perform'

	def ready(self):
		import perform.signals
