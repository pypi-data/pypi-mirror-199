import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from settings_app.decorators import allowed_users
from recruitment2.models import Candidate, Plan, PlanPos, Painel

@login_required
@allowed_users(allowed_roles=['hr','hr_s','de','deputy'])
def printRecCandResult(request, hashid, pk):
	group = request.user.groups.all()[0].name
	plan = get_object_or_404(Plan, hashed=hashid)
	planpos = get_object_or_404(PlanPos, pk=pk)
	objects = Candidate.objects.filter(plan=plan, plan_pos=planpos).prefetch_related('candscore').all()\
		.order_by('candscore__sort','id')
	teams = Painel.objects.filter(plan=plan, plan_pos=planpos).all()
	context = {
		'group': group, 'plan': plan, 'planpos': planpos, 'objects': objects, 'teams': teams,
		'title': f'Lista Resultadu', 'legend': f'Lista Resultadu'
	}
	return render(request, 'recruitment2_print/result_print.html', context)
