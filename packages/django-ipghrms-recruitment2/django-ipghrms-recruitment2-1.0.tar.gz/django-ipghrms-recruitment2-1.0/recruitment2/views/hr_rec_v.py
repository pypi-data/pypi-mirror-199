from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from recruitment2.models import Aspect, Plan, PlanPos, PlanPosAspect, PlanTrack, Painel, PlanUnit, PlanAttach
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecPlanList(request):
	group = request.user.groups.all()[0].name
	objects = Plan.objects.filter().prefetch_related('plantrack').all().order_by('-pk')
	context = {
		'group': group, 'objects': objects,
		'title': f'Lista Planu Rekrutamentu', 'legend': f'Lista Planu Rekrutamentu'
	}
	return render(request, 'recruitment2/hr_plan_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecPlanDetail(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	track = PlanTrack.objects.filter(plan=plan).first()
	planposs = PlanPos.objects.filter(plan=plan).all()
	teams = Painel.objects.filter(plan=plan).all()
	planunit = PlanUnit.objects.filter(plan=plan).all()
	planattach = PlanAttach.objects.filter(plan=plan).all()
	context = {
		'group': group, 'plan': plan, 'track': track, 'planposs': planposs, 'teams': teams,
		'title': f'Detalha Planu Rekrutamentu', 'legend': f'Detalha Planu Rekrutamentu',  'planattach':planattach,
		'planunit':planunit
	}
	return render(request, 'recruitment2/hr_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecPlanPosDetail(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	track = PlanTrack.objects.filter(plan=plan).first()
	posasps = Aspect.objects.filter().all().order_by('id')
	teams = Painel.objects.filter(plan=plan, plan_pos=planpos).all()
	objects = []
	for i in posasps:
		a = PlanPosAspect.objects.filter(plan=plan, plan_pos=planpos, aspect=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'plan': plan, 'track': track, 'planpos': planpos, 'objects': objects, 'teams': teams,
		'title': f'Lista Pojisaun ba {planpos.position}', 'legend': f'Lista Pojisaun ba {planpos.position}'
	}
	return render(request, 'recruitment2/hr_plan_pos_detail.html', context)

