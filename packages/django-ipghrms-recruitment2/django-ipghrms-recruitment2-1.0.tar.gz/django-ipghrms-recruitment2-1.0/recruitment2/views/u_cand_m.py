import datetime, numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from django.contrib import messages
from recruitment2.models import CandShortList, CandOral, CandWritten, Candidate, Plan, PlanPos, Painel, PlanTrack
from recruitment2.forms import CandShortListForm2, CandWrittenForm2, CandOralForm2
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecShortListAdd(request, hashid, hashid2, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	u_painel = get_object_or_404(Painel, pk=pk)
	planpos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandShortList)
		form = CandShortListForm2(request.POST)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.1
			score_b = float(form.cleaned_data.get('score_b')) * 0.2
			score_c = float(form.cleaned_data.get('score_c')) * 0.4
			score_d = float(form.cleaned_data.get('score_d')) * 0.3
			check = CandShortList.objects.filter(plan=plan, painel__plan_pos=planpos, candidate=cand, user=request.user).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.painel = u_painel
			instance.total = score_a+score_b+score_c+score_d
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)
	else: form = CandShortListForm2()
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand,
		'u_painel': u_painel, 'page': 'pcanddet',
		'title': 'Aumenta Valor Shortlist', 'legend': 'Aumenta Valor Shortlist'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit',  'deputy', 'de'])
def uRecShortListUpdate(request, pk,pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandShortList, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	plan = objects.plan
	cand = objects.candidate
	planpos = cand.plan_pos
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
			return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed, pk=u_painel.id)
	else: form = CandShortListForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand, 'page': 'pcanddet',
		'u_painel': u_painel,
		'title': 'Altera Valor Shortlist', 'legend': 'Altera Valor Shortlist'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecShortListDel(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandShortList, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)
###
@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecWrittenAdd(request, hashid, hashid2, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	u_painel = get_object_or_404(Painel, pk=pk)
	planpos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandWritten)
		form = CandWrittenForm2(request.POST, request.FILES)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.2
			score_b = float(form.cleaned_data.get('score_b')) * 0.7
			score_c = float(form.cleaned_data.get('score_c')) * 0.1
			check = CandWritten.objects.filter(plan=plan, painel__plan_pos=planpos, painel=u_painel, candidate=cand).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed, pk=u_painel.id)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.painel = u_painel
			instance.total = score_a+score_b+score_c
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)
	else: form = CandWrittenForm2()
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand, 'u_painel': u_painel, 'page': 'pcanddet',
		'title': 'Aumenta Valor Eskrita', 'legend': 'Aumenta Valor Eskrita'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecWrittenUpdate(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandWritten, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	plan = objects.plan
	cand = objects.candidate
	planpos = cand.plan_pos
	if request.method == 'POST':
		form = CandWrittenForm2(request.POST, request.FILES, instance=objects)
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
			return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed, pk=u_painel.id)
	else: form = CandWrittenForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand, 'u_painel': u_painel, 'page': 'pcanddet',
		'title': 'Altera Valor Eskrita', 'legend': 'Altera Valor Eskrita'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecWrittenDel(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandWritten, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)
###
@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecOralAdd(request, hashid, hashid2, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	cand = get_object_or_404(Candidate, hashed=hashid2)
	u_painel = get_object_or_404(Painel, pk=pk)
	planpos = cand.plan_pos
	if request.method == 'POST':
		newid, new_hashid = getnewid(CandOral)
		form = CandOralForm2(request.POST, request.FILES)
		if form.is_valid():
			score_a = float(form.cleaned_data.get('score_a')) * 0.15
			score_b = float(form.cleaned_data.get('score_b')) * 0.25
			score_c = float(form.cleaned_data.get('score_c')) * 0.35
			score_d = float(form.cleaned_data.get('score_d')) * 0.15
			score_e = float(form.cleaned_data.get('score_c')) * 0.1
			check = CandOral.objects.filter(plan=plan, painel__plan_pos=planpos, painel=u_painel, candidate=cand).first()
			if check:
				messages.warning(request, f'valor painel iha ona.')
				return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed, pk=u_painel.id)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.candidate = cand
			instance.painel = u_painel
			instance.total = score_a+score_b+score_c+score_d+score_e
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)
	else: form = CandOralForm2()
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand, 'u_painel': u_painel, 'page': 'pcanddet',
		'title': 'Aumenta Valor', 'legend': 'Aumenta Valor'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecOralUpdate(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandOral, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	plan = objects.plan
	cand = objects.candidate
	planpos = cand.plan_pos
	if request.method == 'POST':
		form = CandOralForm2(request.POST, instance=objects)
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
			return redirect('rec2-u-cand-detail', hashid=plan.hashed, hashid2=cand.hashed, pk=u_painel.id)
	else: form = CandOralForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos, 'cand': cand, 'u_painel':u_painel, 'page': 'pcanddet',
		'title': 'Altera Valor', 'legend': 'Altera Valor'
	}
	return render(request, 'recruitment2/u_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','staff','dep','unit', 'deputy', 'de'])
def uRecOralDel(request, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(CandOral, pk=pk)
	u_painel = get_object_or_404(Painel, pk=pk2)
	hashid = objects.plan.hashed
	hashid2 = objects.candidate.hashed
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-u-cand-detail', hashid=hashid, hashid2=hashid2, pk=u_painel.id)