from django.apps import AppConfig


class Recruitment2Config(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'recruitment2'

	def ready(self):
		import recruitment2.signals
