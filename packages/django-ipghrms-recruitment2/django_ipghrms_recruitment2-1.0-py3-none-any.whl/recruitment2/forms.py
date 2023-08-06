from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from recruitment2.models import *
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
	input_type = 'date'


class PlanUnitForm(forms.ModelForm):
	class Meta:
		model = PlanUnit
		fields = ['units']
		widgets = {
			'units': forms.CheckboxSelectMultiple(),
		}

	units = forms.ModelMultipleChoiceField(
		queryset=Unit.objects.all(),
		widget=forms.CheckboxSelectMultiple(),
		label = 'Hili Divizaun'
	)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('units', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class PlanUnitUpdateForm(forms.ModelForm):
	class Meta:
		model = PlanUnit
		fields = ['units']
		widgets = {
			'units': forms.CheckboxSelectMultiple(),
		}

	units = forms.ModelMultipleChoiceField(
		queryset=Unit.objects.all(),
		widget=forms.CheckboxSelectMultiple(),
	)

	def __init__(self, *args, **kwargs):
		plan = kwargs.pop('plan', None)
		super().__init__(*args, **kwargs)
		if plan is not None:
			self.fields['units'].initial = [pu.unit for pu in plan.planunit_set.all()]
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('units', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class PlanForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(), required=False)
	class Meta:
		model = Plan
		fields = ['description','objective','date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['date'].label = 'Data Plano Rekrutamento'
		self.fields['description'].required = True
		self.fields['date'].required = True
		self.fields['objective'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('description', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('objective', css_class='form-group col-md-6 mb-0'),
				Column('date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanAttachForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(), required=False)
	class Meta:
		model = PlanAttach
		fields = ['name','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['name'].required = True
		self.fields['file'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('file', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanPosForm(forms.ModelForm):
	class Meta:
		model = PlanPos
		fields = ['number','position','total','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['position'].label = 'Pojisaun'
		self.fields['number'].required = True
		self.fields['position'].required = True
		self.fields['total'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('position', css_class='form-group col-md-3 mb-0'),
				Column('total', css_class='form-group col-md-2 mb-0'),
				Column('file', css_class='form-group col-md-7 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanPosAspForm(forms.ModelForm):
	class Meta:
		model = PlanPosAspect
		fields = ['aspectops']
	def __init__(self, pk, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['aspectops'].queryset = AspectOps.objects.filter(aspect_id=pk).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('aspectops', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanRejectForm(forms.ModelForm):
	class Meta:
		model = PlanTrack
		fields = ['reject_comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('reject_comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class PainelForm(forms.ModelForm):
	class Meta:
		model = Painel
		fields = ['employee','position']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-6 mb-0'),
				Column('position', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandidateForm(forms.ModelForm):
	date = forms.DateField(label='Data Registu', widget=DateInput(), required=False)
	class Meta:
		model = Candidate
		fields = ['plan_pos','name','sex','phone','email','date','university','diploma']
	def __init__(self, *args, **kwargs):
		hashid = kwargs.pop('hashid', None)
		super().__init__(*args, **kwargs)
		if hashid:
			self.fields['plan_pos'].queryset = PlanPos.objects.filter(plan__hashed=hashid)
		self.helper = FormHelper()
		self.fields['plan_pos'].required = True
		self.fields['name'].required = True
		self.fields['phone'].required = True
		self.fields['date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('plan_pos', css_class='form-group col-md-3 mb-0'),
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('sex', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('phone', css_class='form-group col-md-3 mb-0'),
				Column('email', css_class='form-group col-md-6 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('university', css_class='form-group col-md-6 mb-0'),
				Column('diploma', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandShortListForm(forms.ModelForm):
	comment_a = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_b = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_c = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_d = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	class Meta:
		model = CandShortList
		fields = ['painel','score_a','score_b','score_c','score_d','comment_a']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('painel', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_a', css_class='form-group col-md-3 mb-0'),
				Column('comment_a', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_b', css_class='form-group col-md-3 mb-0'),
				Column('comment_b', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_c', css_class='form-group col-md-3 mb-0'),
				Column('comment_c', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_d', css_class='form-group col-md-3 mb-0'),
				Column('comment_d', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandShortListForm2(forms.ModelForm):
	comment_a = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_b = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_c = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	comment_d = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	class Meta:
		model = CandShortList
		fields = ['score_a','score_b','score_c','score_d','comment_a','comment_b','comment_c','comment_d']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('score_a', css_class='form-group col-md-3 mb-0'),
				Column('comment_a', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_b', css_class='form-group col-md-3 mb-0'),
				Column('comment_b', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_c', css_class='form-group col-md-3 mb-0'),
				Column('comment_c', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_d', css_class='form-group col-md-3 mb-0'),
				Column('comment_d', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandCVForm(forms.ModelForm):
	class Meta:
		model = CandidateCv
		fields = ['file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['file'].required = True
		self.helper.layout = Layout(
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandSummaryForm(forms.ModelForm):
	summary = forms.CharField(label="Komentario", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	class Meta:
		model = CandidateShorListSum
		fields = ['short_list_type', 'summary']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('short_list_type', css_class='form-group col-md-4 mb-0'),
				Column('summary', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandSummaryForm2(forms.ModelForm):
	summary = forms.CharField(label="Komentario", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}))
	class Meta:
		model = CandidateShorListSum
		fields = ['summary']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('summary', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandWrittenForm(forms.ModelForm):
	class Meta:
		model = CandWritten
		fields = ['painel','score_a','score_b','score_c', 'file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('painel', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_a', css_class='form-group col-md-3 mb-0'),
				Column('score_b', css_class='form-group col-md-3 mb-0'),
				Column('score_c', css_class='form-group col-md-3 mb-0'),
				Column('file', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandWrittenForm2(forms.ModelForm):
	class Meta:
		model = CandWritten
		fields = ['score_a','score_b','score_c', 'file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('score_a', css_class='form-group col-md-4 mb-0'),
				Column('score_b', css_class='form-group col-md-4 mb-0'),
				Column('score_c', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class CandOralForm(forms.ModelForm):
	class Meta:
		model = CandOral
		fields = ['painel','score_a','score_b','score_c','score_d','score_d','score_e', 'file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('painel', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_a', css_class='form-group col-md-4 mb-0'),
				Column('score_b', css_class='form-group col-md-4 mb-0'),
				Column('score_c', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_d', css_class='form-group col-md-4 mb-0'),
				Column('score_e', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandOralForm2(forms.ModelForm):
	class Meta:
		model = CandOral
		fields = ['score_a','score_b','score_c','score_d','score_d','score_e', 'file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('score_a', css_class='form-group col-md-4 mb-0'),
				Column('score_b', css_class='form-group col-md-4 mb-0'),
				Column('score_c', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('score_d', css_class='form-group col-md-4 mb-0'),
				Column('score_e', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CandFinalDesForm(forms.ModelForm):
	class Meta:
		model = CandScore
		fields = ['obs']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)