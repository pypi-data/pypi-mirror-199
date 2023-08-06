import datetime, numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from django.contrib import messages
from recruitment2.models import CandShortList, CandOral, CandScore, CandWritten, Candidate, Plan, PlanPos, Painel, PlanTrack
from recruitment2.forms import CandShortListForm, CandShortListForm2, CandFinalDesForm, CandidateForm, PainelForm
from settings_app.utils import getnewid

###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecTeamAdd(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	if request.method == 'POST':
		newid, _ = getnewid(Painel)
		form = PainelForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			pos = request.POST.get('position')
			allpainel = Painel.objects.filter(plan=plan, plan_pos=planpos, position=pos).exists()
			if allpainel == False:

				instance.id = newid
				instance.plan = plan
				instance.plan_pos = planpos
				instance.save()
				messages.success(request, f'Aumenta sucessu.')
				return redirect('rec2-hr-planpos-detail', hashid=hashid, pk=pk)
			else:
				messages.error(request, f'Painel {pos} Iha Ona.')
				return redirect('rec2-hr-planpos-detail', hashid=hashid, pk=pk)

	else: form = PainelForm()
	context = {
		'group': group, 'form': form, 'plan': plan,
		'title': 'Aumenta Painel', 'legend': 'Aumenta Painel'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecTeamUpdate(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	objects = get_object_or_404(Painel, pk=pk)
	planpos = objects.plan_pos
	if request.method == 'POST':
		form = PainelForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-planpos-detail', hashid=hashid, pk=planpos.id)
	else: form = PainelForm(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan,
		'title': 'Altera Ekipa', 'legend': 'Altera Ekipa'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecTeamDelete(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Painel, pk=pk)
	planpos = objects.plan_pos
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-planpos-detail', hashid=hashid, pk=planpos.id)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandAdd(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Candidate)
		form = CandidateForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-cand-list', hashid=hashid)
	else: form = CandidateForm(hashid=hashid)
	context = {
		'group': group, 'form': form, 'plan': plan, 'page': 'pcand',
		'title': 'Aumenta Kandidatu', 'legend': 'Aumenta Kandidatu', 'legend2': 'Formulario Aumenta Kandidatu'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandUpdate(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	objects = get_object_or_404(Candidate, hashed=hashid2)
	if request.method == 'POST':
		form = CandidateForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-cand-list', hashid=hashid)
	else: form = CandidateForm(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'page': 'pcand',
		'title': 'Altera Kandidatu', 'legend': 'Altera Kandidatu'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandDelete(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Candidate, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-cand-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecCandLock(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Candidate, pk=pk)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Taka.')
	return redirect('rec2-hr-cand-detail', hashid=objects.plan.hashed, hashid2=objects.hashed)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecShortListAdd(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandShortList)
		form = CandShortListForm(request.POST)
		if form.is_valid():
			painel = form.cleaned_data.get('painel')
			score_a = float(form.cleaned_data.get('score_a')) * 0.1
			score_b = float(form.cleaned_data.get('score_b')) * 0.2
			score_c = float(form.cleaned_data.get('score_c')) * 0.4
			score_d = float(form.cleaned_data.get('score_d')) * 0.3
			check = CandShortList.objects.filter(plan=plan, painel__plan_pos=plan_pos, painel=painel, candidate=cand).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.total = score_a+score_b+score_c+score_d
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)
	else: form = CandShortListForm()
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Aumenta Valor Shortlist', 'legend': 'Aumenta Valor Shortlist'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecShortListUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandShortList, pk=pk)
	plan = objects.plan
	cand = objects.candidate
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		form = CandShortListForm2(request.POST, instance=objects)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.1
			score_b = float(form.cleaned_data.get('score_b')) * 0.2
			score_c = float(form.cleaned_data.get('score_c')) * 0.4
			score_d = float(form.cleaned_data.get('score_d')) * 0.3
			instance = form.save(commit=False)
			instance.total = score_a+score_b+score_c+score_d
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
	else: form = CandShortListForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Altera Valor Shortlist', 'legend': 'Altera Valor Shortlist'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecShortListDel(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandShortList, pk=pk)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)

@login_required
@allowed_users(allowed_roles=['hr','staff'])
def uRecShortListDel(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandShortList, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecScoreRef(request, hashid):
	group = request.user.groups.all()[0].name
	cand = get_object_or_404(Candidate, hashed=hashid)
	planpos = cand.plan_pos
	tot_painels = Painel.objects.filter(plan_pos=planpos).count()
	tot_a, tot_b, tot_c = 0,0,0
	obj_a = CandShortList.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	if obj_a: 
		tot_a = obj_a
		tot_a = float(tot_a)/float(tot_painels)
	obj_b = CandWritten.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	if obj_b: 
		tot_b = obj_b
		tot_b = float(tot_b)/float(tot_painels)
	obj_c = CandOral.objects.filter(candidate=cand).aggregate(Sum('total')).get('total__sum', 0.00)
	if obj_c: 
		tot_c = obj_c
		tot_c = float(tot_c)/float(tot_painels)
	candscore = CandScore.objects.filter(candidate=cand).first()
	candscore.score_a = tot_a
	candscore.score_b = tot_b
	candscore.score_c = tot_c
	candscore.final_score = (float(tot_a)*0.1 + float(tot_b)*0.4 + float(tot_c)*0.5)
	candscore.save()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-cand-detail', hashid=cand.plan.hashed, hashid2=hashid)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecFinalDec(request, hashid):
	group = request.user.groups.all()[0].name
	cand = get_object_or_404(Candidate, hashed=hashid)
	plan = cand.plan
	objects = CandScore.objects.filter(candidate=cand).first()
	if request.method == 'POST':
		form = CandFinalDesForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
	else: form = CandFinalDesForm(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Decijaun Final', 'legend': 'Decijaun Final'
	}
	return render(request, 'recruitment2/hr_form.html', context)
###
@login_required
@allowed_users(allowed_roles=['hr'])
def RecPlanTrackFinish(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	plan = objects.plan
	objects.is_finish = True
	objects.save()
	plan.is_active = False
	plan.save()
	messages.success(request, f'Publika ona.')
	return redirect('rec2-hr-plan-detail', hashid=objects.plan.hashed)