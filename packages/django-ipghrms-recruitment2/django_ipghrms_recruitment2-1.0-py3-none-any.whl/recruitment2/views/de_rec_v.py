from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from recruitment2.models import Aspect, Plan, PlanPos, PlanPosAspect, PlanTrack, Candidate, CandShortList,\
	CandScore, CandOral, CandWritten, Painel, PlanUnit, PlanAttach
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deRecPlanList(request):
	group = request.user.groups.all()[0].name
	objects = Plan.objects.filter().prefetch_related('plantrack').all().order_by('-date','id')
	context = {
		'group': group, 'objects': objects,
		'title': f'Lista Planu Rekrutamentu', 'legend': f'Lista Planu Rekrutamentu'
	}
	return render(request, 'recruitment2/de_plan_list.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deRecPlanDetail(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	track = PlanTrack.objects.filter(plan=plan).first()
	planposs = PlanPos.objects.filter(plan=plan).all()
	teams = Painel.objects.filter(plan=plan).all()
	planunit = PlanUnit.objects.filter(plan=plan).all()
	planattach = PlanAttach.objects.filter(plan=plan).all()
	context = {
		'group': group, 'plan': plan, 'track': track, 'planposs': planposs, 'teams': teams,
		'title': f'Detalha Planu Rekrutamentu', 'legend': f'Detalha Planu Rekrutamentu', 'planattach':planattach,
		'planunit':planunit
	}
	return render(request, 'recruitment2/de_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deRecPlanPosDetail(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	track = PlanTrack.objects.filter(plan=plan).first()
	planpos = get_object_or_404(PlanPos, pk=pk)
	aspects = Aspect.objects.filter().all().order_by('id')
	objects = []
	for i in aspects:
		a = PlanPosAspect.objects.filter(plan=plan, plan_pos=planpos, aspect=i).all()
		objects.append([i,a])
	teams = Painel.objects.filter(plan=plan, plan_pos=planpos).all()
	context = {
		'group': group, 'plan': plan, 'track': track, 'planpos': planpos, 'objects': objects, 'teams': teams,
		'title': f'Lista Pojisaun ba {planpos.position}', 'legend': f'Lista Pojisaun ba {planpos.position}'
	}
	return render(request, 'recruitment2/de_plan_pos_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deRecCandList(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	objects = Candidate.objects.filter(plan=plan).prefetch_related('candscore').all().order_by('id')
	context = {
		'group': group, 'objects': objects, 'plan': plan,
		'title': f'Lista Kandidatu', 'legend': f'Lista Kandidatu'
	}
	return render(request, 'recruitment2/de_cand_list.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deRecCandDetail(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	planpos = cand.plan_pos
	candscore = CandScore.objects.get(candidate=cand)
	shortlists = CandShortList.objects.filter(candidate=cand).all()
	writtens = CandWritten.objects.filter(candidate=cand).all()
	orals = CandOral.objects.filter(candidate=cand).all()
	tot_a = CandShortList.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_b = CandWritten.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_c = CandOral.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	context = {
		'group': group, 'plan': plan, 'cand': cand, 'candscore': candscore,
		'shortlists': shortlists, 'writtens': writtens, 'orals': orals,
		'tot_a': tot_a, 'tot_b': tot_b, 'tot_c': tot_c,
		'title': f'Detalha Kandidatu', 'legend': f'Detalha Kandidatu'
	}
	return render(request, 'recruitment2/de_cand_detail.html', context)
###
@login_required
# @allowed_users(allowed_roles=['de','deputy'])
def deRecCandResultList(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).prefetch_related('candscore').all()\
		.order_by('candscore__sort','id')
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'objects': objects,
		'title': f'Lista Resultadu', 'legend': f'Lista Resultadu'
	}
	return render(request, 'recruitment2/de_cand_result_list.html', context)

@login_required
# @allowed_users(allowed_roles=['de','deputy'])
def deRecCandResultDet(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	cand = get_object_or_404(Candidate, pk=pk2)
	candscore = CandScore.objects.get(candidate=cand)
	shortlists = CandShortList.objects.filter(candidate=cand).all()
	writtens = CandWritten.objects.filter(candidate=cand).all()
	orals = CandOral.objects.filter(candidate=cand).all()
	tot_a = CandShortList.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_b = CandWritten.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_c = CandOral.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'cand': cand, 'candscore': candscore,
		'shortlists': shortlists, 'writtens': writtens, 'orals': orals,
		'tot_a': tot_a, 'tot_b': tot_b, 'tot_c': tot_c,
		'title': f'Detalha Kandidatu', 'legend': f'Detalha Kandidatu'
	}
	return render(request, 'recruitment2/de_cand_result_det.html', context)