import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from settings_app.decorators import allowed_users
from recruitment2.models import CandShortList, CandOral, CandScore, CandWritten, Candidate, Plan, PlanPos, \
	CandidateCv, CandidateShorListSum, ShortListType
from django.conf import settings
from django.http import FileResponse, Http404

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandList(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	objects = Candidate.objects.filter(plan=plan).prefetch_related('candscore').all().order_by('id')
	context = {
		'group': group, 'objects': objects, 'plan': plan,
		'title': f'Lista Kandidatu', 'legend': f'Lista Kandidatu'
	}
	return render(request, 'recruitment2/hr_cand_list.html', context)


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCvList(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	data = []
	objects = Candidate.objects.filter(plan=plan).prefetch_related('candscore').all().order_by('id')
	for obj in  objects:
		cv = CandidateCv.objects.filter(candidate=obj).last()
		summary = CandidateShorListSum.objects.filter(candidate=obj)
		data.append([obj, cv, summary])
	context = {
		'group': group, 'objects': data, 'plan': plan,
		'title': f'Lista CV no  Sumariu Shorlist', 'legend': f'Lista CV no  Sumariu Shorlist'
	}
	return render(request, 'recruitment2/hr_cand_cv_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecsSumList(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid2)
	objects = Candidate.objects.get(hashed=hashid)
	shorlist = ShortListType.objects.all()
	summary = CandidateShorListSum.objects.filter(candidate=objects)
	context = {
		'group': group, 'objects': summary, 'plan': plan, 'candidate':objects,
		'title': f'Lista Sumariu Shorlist', 'legend': f'Lista Sumariu Shorlist', 'shorlist':shorlist
	}
	return render(request, 'recruitment2/hr_cand_sum_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandDetail(request, hashid, hashid2):
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
	return render(request, 'recruitment2/hr_cand_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandResultList(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).prefetch_related('candscore').all()\
		.order_by('candscore__sort','id')
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'objects': objects,
		'title': f'Lista Resultadu', 'legend': f'Lista Resultadu', 'p1': 'p1', 'p2': 'p2', 'p3': 'p3'
	}
	return render(request, 'recruitment2/hr_cand_result_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandResultShortList(request, hashid, pk, page):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	if page == 'p1':
		title = 'Short List Process'
		legend = 'Short List Process'
	if page == 'p2':
		title = 'Written Test'
		legend = 'Written Test'
	if page == 'p3':
		title = 'Interview Test'
		legend = 'Interview Test'
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).prefetch_related('candscore').all()\
		.order_by('candscore__sort','id')
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'objects': objects,
		'title': title, 'legend': legend, 'p1': 'p1', 'p2': 'p2', 'p3': 'p3', 'page':page
	}
	return render(request, 'recruitment2/hr_cand_result.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandResultDet(request, hashid, pk, pk2):
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
	return render(request, 'recruitment2/hr_cand_result_det.html', context)


@login_required
def RecCandCV(request, pk):
	objects = get_object_or_404(CandidateCv, pk=pk)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')