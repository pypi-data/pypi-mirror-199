import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from settings_app.decorators import allowed_users
from recruitment2.models import CandShortList, CandOral, \
	 PlanAttach, CandScore, CandWritten, Candidate, Plan, PlanPos, Painel, CandidateCv, CandidateShorListSum, ShortListType

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecCandList(request, pk, pk2):
	group = request.user.groups.all()[0].name
	planpos = get_object_or_404(PlanPos, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	plan = planpos.plan
	att = PlanAttach.objects.filter(plan=plan)
	data = []
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).order_by('id')
	for cand in objects:
		shortlists = CandShortList.objects.filter(candidate=cand, painel=u_painel).exists()
		writtens = CandWritten.objects.filter(candidate=cand, painel=u_painel).exists()
		orals = CandOral.objects.filter(candidate=cand, painel=u_painel).exists()
		data.append([cand, shortlists, writtens, orals])
	context = {
		'group': group, 'objects': data, 'plan': plan, 'u_painel': u_painel,
		'title': f'Lista Kandidatu', 'legend': f'Lista Kandidatu', 'att':att
	}
	return render(request, 'recruitment2/u_cand_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit',  'deputy', 'de'])
def uRecCandDetail(request, hashid, hashid2, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	u_painel = get_object_or_404(Painel, pk=pk)
	planpos = cand.plan_pos
	shortlists = CandShortList.objects.filter(candidate=cand, painel=u_painel).all()
	writtens = CandWritten.objects.filter(candidate=cand, painel=u_painel).all()
	orals = CandOral.objects.filter(candidate=cand, painel=u_painel).all()
	tot_a = CandShortList.objects.filter(candidate=cand, painel=u_painel).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_b = CandWritten.objects.filter(candidate=cand, painel=u_painel).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_c = CandOral.objects.filter(candidate=cand, painel=u_painel).aggregate(Sum('total')).get('total__sum', 0.00)
	cv = CandidateCv.objects.filter(candidate=cand).last()
	shorlist = ShortListType.objects.all()
	summary = CandidateShorListSum.objects.filter(candidate=cand)
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'u_painel': u_painel, 'cand': cand,
		'shortlists': shortlists, 'writtens': writtens, 'orals': orals,
		'tot_a': tot_a, 'tot_b': tot_b, 'tot_c': tot_c, 'cv': cv,
		'title': f'Detalha Kandidatu', 'legend': f'Detalha Kandidatu',
		'shorlist':shorlist, 'summary':summary
	}
	return render(request, 'recruitment2/u_cand_detail.html', context)
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def RecFileCandWriPDF(request, hashid):
	objects = get_object_or_404(CandWritten, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')
@login_required
def RecFileCandOralPDF(request, hashid):
	objects = get_object_or_404(CandOral, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')