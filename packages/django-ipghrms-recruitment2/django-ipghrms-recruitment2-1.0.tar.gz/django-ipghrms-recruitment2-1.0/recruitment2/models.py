from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import Unit
from employee.models import Employee
from contract.models import Category
from .utils import upload_rec_tor, upload_rec_prop,upload_can_cv, upload_rec_attach, upload_rec_written, upload_rec_oral

class Objective(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Position(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Aspect(models.Model):
	name = models.CharField(max_length=20, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AspectOps(models.Model):
	aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=20, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Diploma(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
#
class Plan(models.Model):
	description = models.CharField(max_length=150, null=True, blank=True, verbose_name="Deskrisaun")
	objective = models.ForeignKey(Objective, on_delete=models.CASCADE, null=True, blank=True, related_name="plan", verbose_name="Objetivu")
	date = models.DateField(null=True, blank=True)
	file = models.FileField(upload_to=upload_rec_prop, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Proposal")
	is_active = models.BooleanField(default=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.description}-{0.objective} - {0.date}'
		return template.format(self)

class PlanUnit(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name="planunit", verbose_name="Divizaun")
	def __str__(self):
		template = '{0.plan} - {0.unit}'
		return template.format(self)


class PlanTrack(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="plantrack")
	is_lock = models.BooleanField(default=False, null=True)
	is_send = models.BooleanField(default=False, null=True)
	is_approve = models.BooleanField(default=False, null=True)
	is_publish = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	reject_comment = models.TextField(null=True, blank=True)
	def __str__(self):
		template = '{0.plan} - L:{0.is_lock}/S:{0.is_send}/A:{0.is_approve}/P:{0.is_publish}/F:{0.is_finish}'
		return template.format(self)

class PlanPos(models.Model):
	number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Vacancy Tracking Number")
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="planpos")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="planpos")
	total = models.IntegerField(null=True, blank=True)
	file = models.FileField(upload_to=upload_rec_tor, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach ToR")
	is_lock = models.BooleanField(default=False, null=True)
	def __str__(self):
		template = '{0.position}'
		return template.format(self)

class PlanPosAspect(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="planposaspect")
	plan_pos = models.ForeignKey(PlanPos, on_delete=models.CASCADE, null=True, blank=True, related_name="planposaspect", verbose_name="Kategoria")
	aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Aspetu")
	aspectops = models.ForeignKey(AspectOps, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kriteria")
	def __str__(self):
		template = '{0.aspect} - {0.aspectops}'
		return template.format(self)
#
class TeamPos(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class ShortListType(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	sub = models.CharField(max_length=100, null=True, blank=True)
	percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Painel(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="painel")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="painel")
	position = models.ForeignKey(TeamPos, on_delete=models.CASCADE, null=True, blank=True, related_name="painel")
	plan_pos = models.ForeignKey(PlanPos, on_delete=models.CASCADE, null=True, blank=True, related_name="painel")
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="painel")
	is_active = models.BooleanField(default=False, null=True)
	def __str__(self):
		template = '{0.employee} - {0.position}'
		return template.format(self)

class PlanAttach(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="planAttach")
	name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
	file = models.FileField(upload_to=upload_rec_attach, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anekso")
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.plan} - {0.name}'
		return template.format(self)
#
class Schedule(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="schedule")
	date = models.DateField(null=True, blank=True)
	subject = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self):
		template = '{0.plan} - {0.date}'
		return template.format(self)
#
class Candidate(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="candidate")
	plan_pos = models.ForeignKey(PlanPos, on_delete=models.CASCADE, null=True, blank=True, related_name="candidate", verbose_name='Pojisaun')
	name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Naran Kandidatu")
	sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=False, verbose_name="Sexu")
	phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="No. Kontaktu")
	email = models.CharField(max_length=20, null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	university = models.CharField(max_length=200, null=True, blank=True, verbose_name="Universidade")
	diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, null=True, blank=True, related_name="candidate")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	is_ready = models.BooleanField(default=False, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.plan} - {0.name}'
		return template.format(self)

class CandidateCv(models.Model):
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candcv")
	file = models.FileField(upload_to=upload_can_cv, null=True, blank=True,
		validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach CV")
	def __str__(self):
		template = '{0.candidate} - {0.candidate.plan_pos}'
		return template.format(self)

class CandidateShorListSum(models.Model):
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candshorlistsum")
	short_list_type = models.ForeignKey(ShortListType, on_delete=models.CASCADE, null=True, blank=True)
	summary = models.TextField(blank=True, null=True)
	
	def __str__(self):
		template = '{0.candidate} - {0.candidate.plan_pos} - {0.short_list_type}'
		return template.format(self)

class CandScore(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="candscore")
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candscore")
	score_a = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	score_b = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	score_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	obs = models.CharField(choices=[('Passa','Passa'),('La Passa','La Passa')], max_length=10, null=True, blank=False)
	sort = models.IntegerField(null=True, blank=True)
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.candidate.name} - {0.final_score}'
		return template.format(self)

class CandShortList(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="candshortlist")
	painel = models.ForeignKey(Painel, on_delete=models.CASCADE, null=True, blank=True, related_name="candshortlist")
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candshortlist")
	score_a = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Academic Qualification")
	score_b = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Profesisonal Training")
	score_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Professional Experience")
	score_d = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Organizational Experience")
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	comment_a = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
	comment_b = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
	comment_c = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
	comment_d = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.candidate} - {0.total}'
		return template.format(self)

class CandWritten(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="candwritten")
	painel = models.ForeignKey(Painel, on_delete=models.CASCADE, null=True, blank=True, related_name="candwritten")
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candwritten")
	score_a = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="General Questions")
	score_b = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Specific Questions")
	score_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Language Ability Question")
	file = models.FileField(upload_to=upload_rec_written, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anekso")
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.candidate.name} - {0.painel} - {0.total}'
		return template.format(self)

class CandOral(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True, related_name="candoral")
	painel = models.ForeignKey(Painel, on_delete=models.CASCADE, null=True, blank=True, related_name="candoral")
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True, related_name="candoral")
	score_a = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="General Questions")
	score_b = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Academic Experience")
	score_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Professional Experience")
	score_d = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Language Proficiency")
	score_e = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Motivation of Application")
	file = models.FileField(upload_to=upload_rec_oral, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anekso")
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.candidate.name} - {0.painel} - {0.total}'
		return template.format(self)