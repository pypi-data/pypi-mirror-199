import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from recruitment2.models import Aspect, Plan, PlanPos, PlanPosAspect, PlanTrack, PlanUnit, PlanAttach
from recruitment2.forms import PlanPosAspForm, PlanPosForm, PlanForm, PlanRejectForm, PlanUnitForm,PlanUnitUpdateForm, PlanAttachForm
from settings_app.utils import getnewid
from settings_app.user_utils import c_unit

###
@login_required
@allowed_users(allowed_roles=['unit', 'hr'])
def cRecPlanAdd(request):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Plan)
		form = PlanForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.unit = unit
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-plan-detail', instance.hashed)
	else: form = PlanForm()
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Aumenta Planu Rekrutamentu', 'legend': 'Aumenta Planu Rekrutamentu'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit', 'hr'])
def cRecPlanAttachAdd(request, hashid):
	objects = get_object_or_404(Plan, hashed=hashid)
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	if request.method == 'POST':
		form = PlanAttachForm(request.POST, request.FILES)
		if form.is_valid():
			newid, new_hashid = getnewid(PlanAttach)
			instance = form.save(commit=False)
			instance.id = newid
			instance.hashed = new_hashid
			instance.plan = objects
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('rec2-hr-plan-detail', objects.hashed)
	else: form = PlanAttachForm()
	context = {
		'group': group, 'form': form, 'page': 'attach-add', 'plan':objects,
		'title': 'Aumenta Anekso', 'legend': 'Aumenta Anekso'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit', 'hr'])
def cRecPlanAttachUpdate(request, hashid):
	objects = get_object_or_404(PlanAttach, hashed=hashid)
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = PlanAttachForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-plan-detail', objects.plan.hashed)
	else: form = PlanAttachForm(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'attach-add', 'plan':objects,
		'title': 'Altera Anekso', 'legend': 'Altera Anekso'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit', 'hr'])
def cRecPlanAttachDelete(request, hashid, hashid2):
	objects = get_object_or_404(PlanAttach, hashed=hashid)
	objects.delete()
	plan = get_object_or_404(Plan, hashed=hashid2)
	messages.success(request, f'Delete sucessu.')
	return redirect('rec2-hr-plan-detail', plan.hashed)


@login_required
@allowed_users(allowed_roles=['hr'])
def cRecPlanUnitAdd(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		form = PlanUnitForm(request.POST)
		if form.is_valid():
			units = form.cleaned_data['units']
			for unit in units:
				PlanUnit.objects.create(plan=plan, unit=unit)
			return redirect('rec2-hr-plan-detail', hashid)
	else:
		form = PlanUnitForm()
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Aumenta Divizaun ba Planu Rekrutamentu', 'legend': 'Aumenta Divizaun ba Planu Rekrutamentu', 
		'form':form, 'plan':plan
	}
	return render(request, 'recruitment2/form2.html', context)


def cRecPlanUnitUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		form = PlanUnitUpdateForm(request.POST)
		if form.is_valid():
			plan.planunit_set.all().delete()
			units = form.cleaned_data['units']
			for unit in units:
				PlanUnit.objects.create(plan=plan, unit=unit)
			return redirect('rec2-hr-plan-detail', hashid)
	else:
		form = PlanUnitUpdateForm()
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Aumenta Divizaun ba Planu Rekrutamentu', 'legend': 'Aumenta Divizaun ba Planu Rekrutamentu', 
		'form':form, 'plan':plan
	}
	return render(request, 'recruitment2/form2.html', context)




@login_required
@allowed_users(allowed_roles=['hr'])
def cRecPlanUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		form = PlanForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-plan-detail', hashid)
	else: form = PlanForm(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Altera Planu Rekrutamento', 'legend': 'Altera Planu Rekrutamento'
	}
	return render(request, 'recruitment2/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['hr'])
def cRecPlanPosAdd(request, hashid):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(PlanPos)
		form = PlanPosForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-plan-detail', hashid=hashid)
	else: form = PlanPosForm()
	context = {
		'group': group, 'plan': plan, 'form': form, 'page': 'pdetail',
		'title': 'Aumenta Pojisaun', 'legend': 'Aumenta Pojisaun'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def cRecPlanPosUpdate(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	objects = get_object_or_404(PlanPos, pk=pk)
	if request.method == 'POST':
		form = PlanPosForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-hr-plan-detail', hashid=hashid)
	else: form = PlanPosForm(instance=objects)
	context = {
		'group': group, 'plan': plan, 'form': form, 'page': 'pdetail',
		'title': 'Altera Kategoria', 'legend': 'Altera Kategoria'
	}
	return render(request, 'recruitment2/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def cRecPlanPosAspAdd(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	aspect = get_object_or_404(Aspect, pk=pk2)
	if request.method == 'POST':
		newid, _ = getnewid(PlanPosAspect)
		form = PlanPosAspForm(aspect.id, request.POST)
		if form.is_valid():
			aspectops = form.cleaned_data.get('aspectops')
			obj = PlanPosAspect.objects.filter(plan=plan, plan_pos=planpos, aspectops=aspectops).first()
			if obj:
				messages.warning(request, f'Kriteria iha ona.')
				return redirect('rec2-c-planpos-detail', hashid=hashid, pk=pk)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = plan
			instance.plan_pos = planpos
			instance.aspect = aspect
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-c-planpos-detail', hashid=hashid, pk=pk)
	else: form = PlanPosAspForm(aspect.id)
	context = {
		'group': group, 'form': form, 'plan': plan, 'planpos': planpos,
		'aspect': aspect, 'page': 'pposops',
		'title': 'Aumenta Kriteria', 'legend': 'Aumenta Kriteria'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cRecPlanPosAspDelete(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	objects = get_object_or_404(PlanPosAspect, pk=pk2)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('rec2-c-planpos-detail', hashid=hashid, pk=pk)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def RecPlanTrackLock(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Taka.')
	return redirect('rec2-c-plan-detail', hashid=objects.plan.hashed)

@login_required
@allowed_users(allowed_roles=['unit'])
def RecPlanTrackUnLock(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Loke.')
	return redirect('rec2-c-plan-detail', hashid=objects.plan.hashed)

@login_required
@allowed_users(allowed_roles=['unit'])
def RecPlanTrackSend(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	objects.is_send = True
	objects.save()
	messages.success(request, f'Manda ona.')
	return redirect('rec2-c-plan-detail', hashid=objects.plan.hashed)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def RecPlanTrackAppr(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	objects.is_approve = True
	objects.save()
	messages.success(request, f'Aprova ona.')
	return redirect('rec2-de-plan-detail', hashid=objects.plan.hashed)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def RecPlanTrackRej(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	plan = objects.plan
	if request.method == 'POST':
		form = PlanRejectForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.is_send = False
			instance.is_approve = False
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('rec2-de-plan-detail', hashid=plan.hashed)
	else: form = PlanRejectForm(instance=objects)
	context = {
		'group': group, 'plan': plan, 'form': form, 'page': 'preject',
		'title': 'Komentariu Rejeita', 'legend': 'Komentariu Rejeita'
	}
	return render(request, 'recruitment2/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def RecPlanTrackQues(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanPos, pk=pk)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Pergunta sira xavi ona.')
	return redirect('rec2-hr-planpos-detail', hashid=objects.plan.hashed, pk=pk)

@login_required
@allowed_users(allowed_roles=['hr'])
def RecPlanTrackPub(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(PlanTrack, pk=pk)
	objects.is_publish = True
	objects.save()
	messages.success(request, f'Publika ona.')
	return redirect('rec2-hr-plan-detail', hashid=objects.plan.hashed)
