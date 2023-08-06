from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CandScore, Candidate, Plan, PlanTrack

@receiver(post_save, sender=Plan)
def create_plan(sender, instance, created, **kwargs):
	if created:
		PlanTrack.objects.create(id=instance.id, plan=instance, is_approve=True)

@receiver(post_save, sender=Candidate)
def create_cand(sender, instance, created, **kwargs):
	if created:
		CandScore.objects.create(id=instance.id, plan=instance.plan, candidate=instance)
