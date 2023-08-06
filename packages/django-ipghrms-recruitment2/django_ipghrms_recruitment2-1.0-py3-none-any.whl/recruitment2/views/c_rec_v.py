from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from recruitment2.models import Aspect, AspectOps, Plan, PlanPos, PlanPosAspect, PlanTrack, Candidate, PlanAttach
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['unit'])
def cRecPlanList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = Plan.objects.filter(unit=unit).prefetch_related('plantrack').all().order_by('-date','id')
	context = {
		'group': group, 'unit': unit, 'objects': objects,
		'title': f'Lista Planu Rekrutamentu', 'legend': f'Lista Planu Rekrutamentu'
	}
	return render(request, 'recruitment2/c_plan_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cRecPlanDetail(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	track = PlanTrack.objects.filter(plan=plan).first()
	planposs = PlanPos.objects.filter(plan=plan).all()
	context = {
		'group': group, 'plan': plan, 'track': track, 'planposs': planposs,
		'title': f'Detalha Planu Rekrutamentu', 'legend': f'Detalha Planu Rekrutamentu'
	}
	return render(request, 'recruitment2/c_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cRecPlanPosDetail(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	track = PlanTrack.objects.filter(plan=plan).first()
	planpos = get_object_or_404(PlanPos, pk=pk)
	asps = Aspect.objects.filter().all().order_by('id')
	objects = []
	for i in asps:
		a = PlanPosAspect.objects.filter(plan=plan, plan_pos=planpos, aspect=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'plan': plan, 'track': track, 'planpos': planpos, 'objects': objects,
		'title': f'Lista Kriteria ba {planpos.position}', 'legend': f'Lista Kriteria ba {planpos.position}'
	}
	return render(request, 'recruitment2/c_plan_pos_detail.html', context)
###
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def RecPropPDF(request, hashid):
	objects = get_object_or_404(Plan, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')

from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def RecTorPDF(request, pk):
	objects = get_object_or_404(PlanPos, pk=pk)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')


@login_required
def RecFilePDF(request, hashid):
	objects = get_object_or_404(PlanAttach, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')




@login_required
# @allowed_users(allowed_roles=['de','deputy'])
def RecCandResultList(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	# u_painel = get_object_or_404(Painel, pk=pk2)
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).prefetch_related('candscore').all()\
		.order_by('candscore__sort','id')
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'objects': objects,
		'title': f'Lista Candidato no Resultado', 'legend': f'Lista Candidato no Resultado'
	}
	return render(request, 'recruitment2/result_list.html', context)
