import datetime, numpy as np
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from settings_app.decorators import allowed_users
from recruitment2.models import CandShortList, CandOral, CandScore, CandWritten, Candidate, Plan, PlanPos, \
	CandidateCv, CandidateShorListSum, ShortListType, PlanAttach
from recruitment2.forms import CandCVForm, CandSummaryForm,CandSummaryForm2
from settings_app.utils import getnewid
from django.contrib import messages


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandAddCv(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	candidate = get_object_or_404(Candidate, hashed=hashid2)
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		newid,_ = getnewid(CandidateCv)
		form = CandCVForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.candidate = candidate
			instance.save()
			messages.success(request, f'Susesu Aumenta CV')
			return redirect('rec2-hr-cand-cv-list', hashid=hashid)
	else: form = CandCVForm()
	context = {
		'group': group, 'form': form, 'plan': plan, 'page': 'pcand', 'candidate':candidate,
		'title': 'Aumenta CV', 'legend': 'Aumenta CV', 'legend2': 'Formulario Aumenta CV'
	}
	return render(request, 'recruitment2/hr_cand_form.html', context)


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandUpdatCv(request, hashid, hashid2, pk):
    group = request.user.groups.all()[0].name
    objects = CandidateCv.objects.get(pk=pk)
    candidate = get_object_or_404(Candidate, hashed=hashid2)
    plan = get_object_or_404(Plan, hashed=hashid)
    if request.method == 'POST':
        form = CandCVForm(request.POST, request.FILES,instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Susesu Altera CV')
            return redirect('rec2-hr-cand-cv-list', hashid=hashid)
    else: form = CandCVForm(instance=objects)
    context = {
        'group': group, 'form': form, 'plan': plan, 'page': 'pcand', 'candidate':candidate,
        'title': 'Altera CV', 'legend': 'Altera CV', 'legend2': 'Formulario Altera CV'
    }
    return render(request, 'recruitment2/hr_cand_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandAddSummary(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	candidate = get_object_or_404(Candidate, hashed=hashid2)
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		newid,_ = getnewid(CandidateShorListSum)
		form = CandSummaryForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.candidate = candidate
			instance.save()
			messages.success(request, f'Susesu Aumenta CV')
			return redirect('rec2-hr-cand-cv-list', hashid=hashid)
	else: form = CandSummaryForm()
	context = {
		'group': group, 'form': form, 'plan': plan, 'page': 'pcand', 'candidate':candidate,
		'title': 'Aumenta Sumario', 'legend': 'Aumenta Sumario', 'legend2': 'Formulario Aumenta CV'
	}
	return render(request, 'recruitment2/hr_cand_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandAddSummary2(request, hashid, hashid2, pk):
    group = request.user.groups.all()[0].name
    sumid = ShortListType.objects.get(pk=pk)
    candidate = get_object_or_404(Candidate, hashed=hashid2)
    plan = get_object_or_404(Plan, hashed=hashid)
    if request.method == 'POST':
        newid,_ = getnewid(CandidateShorListSum)
        form = CandSummaryForm2(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.candidate = candidate
            instance.short_list_type= sumid
            instance.save()
            messages.success(request, f'Susesu Aumenta Sumario')
            return redirect('rec2-hr-cand-sum-list', hashid=candidate.hashed,hashid2=plan.hashed)
    else: form = CandSummaryForm2()
    context = {
        'group': group, 'form': form, 'plan': plan, 'page': 'pcand', 'candidate':candidate,
        'title': 'Aumenta Sumario', 'legend': 'Aumenta Sumario', 'legend2': 'Formulario Aumenta Sumario', 'sumid':sumid
    }
    return render(request, 'recruitment2/hr_cand_form2.html', context)


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandUpdatSummary(request, hashid, hashid2, pk):
    group = request.user.groups.all()[0].name
    objects = CandidateShorListSum.objects.get(pk=pk)
    candidate = get_object_or_404(Candidate, hashed=hashid2)
    plan = get_object_or_404(Plan, hashed=hashid)
    if request.method == 'POST':
        newid,_ = getnewid(Candidate)
        form = CandSummaryForm(request.POST, request.FILES,instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Susesu Altera Sumario')
            return redirect('rec2-hr-cand-sum-list', hashid=candidate.hashed,hashid2=plan.hashed)
    else: form = CandSummaryForm(instance=objects)
    context = {
        'group': group, 'form': form, 'plan': plan, 'page': 'pcand', 'candidate':candidate,
        'title': 'Altera Sumario', 'legend': 'Altera Sumario', 'legend2': 'Formulario Altera Sumario'
    }
    return render(request, 'recruitment2/hr_cand_form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrCandDeleteSummary(request, hashid, hashid2, pk):
    group = request.user.groups.all()[0].name
    objects = CandidateShorListSum.objects.get(pk=pk)
    candidate = get_object_or_404(Candidate, hashed=hashid2)
    plan = get_object_or_404(Plan, hashed=hashid)
    objects.delete()
    messages.success(request, f'Susesu Delete Sumario')
    return redirect('rec2-hr-cand-sum-list', hashid=candidate.hashed,hashid2=plan.hashed)
