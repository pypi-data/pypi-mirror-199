from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Eval, Evaluator, EvalDate, EvalFinalScore

@receiver(post_save, sender=Eval)
def create_eval(sender, instance, created, **kwargs):
	
	if created:
		Evaluator.objects.create(id=instance.id, eval=instance)
		EvalDate.objects.create(id=instance.id, eval=instance)
		EvalFinalScore.objects.create(id=instance.id, eval=instance)