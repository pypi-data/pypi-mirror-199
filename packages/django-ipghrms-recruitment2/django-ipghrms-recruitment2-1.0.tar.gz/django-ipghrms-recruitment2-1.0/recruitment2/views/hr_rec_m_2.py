import datetime, numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from recruitment2.models import CandOral, CandWritten, Candidate, Plan, PlanPos, CandScore, Painel
from recruitment2.forms import CandOralForm, CandOralForm2, CandWrittenForm, CandWrittenForm2
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecWrittenAdd(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandWritten)
		form = CandWrittenForm(request.POST, request.FILES)
		if form.is_valid():
			painel = form.cleaned_data.get('painel')
			score_a = float(form.cleaned_data.get('score_a')) * 0.2
			score_b = float(form.cleaned_data.get('score_b')) * 0.7
			score_c = float(form.cleaned_data.get('score_c')) * 0.1
			check = CandWritten.objects.filter(plan=plan, painel__plan_pos=plan_pos, painel=painel, candidate=cand).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.total = score_a+score_b+score_c
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)
	else: form = CandWrittenForm()
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Aumenta Valor Eskrita', 'legend': 'Aumenta Valor Eskrita'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecWrittenUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandWritten, pk=pk)
	plan = objects.plan
	cand = objects.candidate
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		form = CandWrittenForm2(request.POST,request.FILES, instance=objects)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.2
			score_b = float(form.cleaned_data.get('score_b')) * 0.7
			score_c = float(form.cleaned_data.get('score_c')) * 0.1
			instance = form.save(commit=False)
			instance.total = score_a+score_b+score_c
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
	else: form = CandWrittenForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Altera Valor Eskrita', 'legend': 'Altera Valor Eskrita'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecWrittenDel(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandWritten, pk=pk)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecOralAdd(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandOral)
		form = CandOralForm(request.POST, request.FILES)
		if form.is_valid():
			painel = form.cleaned_data.get('painel')
			score_a = float(form.cleaned_data.get('score_a')) * 0.15
			score_b = float(form.cleaned_data.get('score_b')) * 0.25
			score_c = float(form.cleaned_data.get('score_c')) * 0.35
			score_d = float(form.cleaned_data.get('score_d')) * 0.15
			score_e = float(form.cleaned_data.get('score_c')) * 0.1
			check = CandOral.objects.filter(plan=plan, painel__plan_pos=plan_pos, painel=painel, candidate=cand).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.total = score_a+score_b+score_c+score_d+score_e
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)
	else: form = CandOralForm()
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Aumenta Valor', 'legend': 'Aumenta Valor'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecOralUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandOral, pk=pk)
	plan = objects.plan
	cand = objects.candidate
	plan_pos = cand.plan_pos
	if request.method == 'POST':
		form = CandOralForm2(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.15
			score_b = float(form.cleaned_data.get('score_b')) * 0.25
			score_c = float(form.cleaned_data.get('score_c')) * 0.35
			score_d = float(form.cleaned_data.get('score_d')) * 0.15
			score_e = float(form.cleaned_data.get('score_c')) * 0.1
			instance = form.save(commit=False)
			instance.total = score_a+score_b+score_c+score_d+score_e
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
	else: form = CandOralForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'cand': cand, 'page': 'pcanddet',
		'title': 'Altera Valor', 'legend': 'Altera Valor'
	}
	return render(request, 'recruitment2/hr_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecOralDel(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandOral, pk=pk)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-hr-cand-detail', hashid=hashid, hashid2=hashid2)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrRecPlanPosSort(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	objects = CandScore.objects.filter(plan=plan, candidate__plan_pos=planpos).all().order_by('-final_score')
	nu = 1
	for i in objects:
		i.sort = nu
		i.save()
		nu = nu + 1 
	messages.success(request, f'Sorting sucessu.')
	return redirect('rec2-hr-cand-result-list', hashid=hashid, pk=pk)
