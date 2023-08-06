from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from employee.models import Employee
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB, EvalDate,\
	EvalSelf, EvalSelfDetA, EvalSelfDetB, EvalPlanningA, EvalPlanningB, EvalPreAssessmentA, EvalPreAssessmentB, EvalPlanning, EvalPreAssessment
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
	input_type = 'date'

class ParameterAForm(forms.ModelForm):
	measure = forms.CharField(label="Measuring", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	criteria = forms.CharField(label="Criteria", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = ParameterA
		fields = ['name','measure','criteria']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('measure', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('criteria', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ParameterBForm(forms.ModelForm):
	indicator = forms.CharField(label="Indicator", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = ParameterB
		fields = ['area','indicator']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('area', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('indicator', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
### EVAL ###
class EvalForm(forms.ModelForm):
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	class Meta:
		model = Eval
		fields = ['employee','start_date','end_date']
	def __init__(self, emp, unit, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter((Q(curempdivision__department__unit=unit)|\
			Q(curempdivision__unit=unit)))\
			.exclude((Q(id=emp.id)|Q(curempdivision__department__id=3)|Q(contract__category_id=6))).all()
		self.helper = FormHelper()
		self.fields['employee'].required = True
		self.fields['start_date'].required = True
		self.fields['end_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-6 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalForm2(forms.ModelForm):
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Ikus', widget=DateInput(), required=False)
	class Meta:
		model = Eval
		fields = ['start_date','end_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalDateForm1(forms.ModelForm):
	date_a_1 = forms.DateField(label='Data Evaluator', widget=DateInput(), required=False)
	date_a_2 = forms.DateField(label='Data Evaluated', widget=DateInput(), required=False)
	class Meta:
		model = EvalDate
		fields = ['date_a_1','date_a_2']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('date_a_1', css_class='form-group col-md-3 mb-0'),
				Column('date_a_2', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalDateForm2(forms.ModelForm):
	date_b_1 = forms.DateField(label='Data Evaluator', widget=DateInput(), required=False)
	date_b_2 = forms.DateField(label='Data Evaluated', widget=DateInput(), required=False)
	class Meta:
		model = EvalDate
		fields = ['date_b_1','date_b_2']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('date_b_1', css_class='form-group col-md-3 mb-0'),
				Column('date_b_2', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalForm4(forms.ModelForm):
	outstanding_perf = forms.CharField(label="Justification Of Outstanding Performance", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['outstanding_perf']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['outstanding_perf'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('outstanding_perf', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalForm5(forms.ModelForm):
	unsatisfactory_perf_obj = forms.CharField(label="Parameter of Individual Objectives", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['unsatisfactory_perf_obj']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['unsatisfactory_perf_obj'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('unsatisfactory_perf_obj', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class EvalForm6(forms.ModelForm):
	unsatisfactory_perf_beh = forms.CharField(label="Parameter of Individual Behaviors", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['unsatisfactory_perf_beh']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['unsatisfactory_perf_beh'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('unsatisfactory_perf_beh', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalForm7(forms.ModelForm):
	recognition_merit = forms.CharField(label="Recognition Of Merit (Outstanding Performance)", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['recognition_merit']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['recognition_merit'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('recognition_merit', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class EvalForm8(forms.ModelForm):
	just_non_evaluation = forms.CharField(label="Justification Of Non-Evaluation", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['just_non_evaluation']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['just_non_evaluation'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('just_non_evaluation', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalForm9(forms.ModelForm):
	comment_next_evaluation = forms.CharField(label="Evaluation, Conditions And / Or Requirements for Personal and professional Development", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalDate
		fields = ['comment_next_evaluation']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['comment_next_evaluation'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment_next_evaluation', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class EvalDetAForm(forms.ModelForm):
	class Meta:
		model = EvalDetA
		fields = ['choice','comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['choice'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('choice', css_class='form-group col-md-3 mb-0'),
				Column('comments', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalDetBForm(forms.ModelForm):
	class Meta:
		model = EvalDetB
		fields = ['choice','comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['choice'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('choice', css_class='form-group col-md-3 mb-0'),
				Column('comments', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class EvalSelfForm(forms.ModelForm):
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	eval_date = forms.DateField(label='Data Avaliasaun', widget=DateInput(), required=False)
	class Meta:
		model = EvalSelf
		fields = ['start_date','end_date','eval_date','comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('start_date', css_class='form-group col-md-4 mb-0'),
				Column('end_date', css_class='form-group col-md-4 mb-0'),
				Column('eval_date', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalSelfForm2(forms.ModelForm):
	comments = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalSelf
		fields = ['comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comments', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalSelfDetAForm(forms.ModelForm):
	comments_a = forms.CharField(label="Goal Exceeded", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	comments_b = forms.CharField(label="Goal Achieved", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	comments_c = forms.CharField(label="Goal Not Reached", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalSelfDetA
		fields = ['comments_a','comments_b','comments_c']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comments_a', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comments_b', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comments_c', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EvalSelfDetBForm(forms.ModelForm):
	comments_a = forms.CharField(label="Demonstrated Competence at a High Level (Explain)", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	comments_b = forms.CharField(label="Demonstrated Competence (Explain)", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	comments_c = forms.CharField(label="Competence not Demonstrated or not existent (Explain)", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalSelfDetB
		fields = ['comments_a','comments_b','comments_c']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comments_a', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comments_b', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comments_c', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class SelfDateForm(forms.ModelForm):
	ind_date = forms.DateField(label='Individual Objective Date', widget=DateInput())
	class Meta:
		model = EvalSelf
		fields = ['ind_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['ind_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('ind_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class SelfDate2Form(forms.ModelForm):
	beh_date = forms.DateField(label='Professional Behavior Date', widget=DateInput())
	class Meta:
		model = EvalSelf
		fields = ['beh_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['beh_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('beh_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class SelfCommentForm(forms.ModelForm):
	comments = forms.CharField(label="Comments", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalSelf
		fields = ['comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['comments'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comments', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

# PLANNING
class PlanningAForm(forms.ModelForm):
	goals = forms.CharField(label="Goal/Activities", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	measuring = forms.CharField(label="Dificulties", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	criteria = forms.CharField(label="Need Improvement", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalPlanningA
		fields = ['goals','measuring', 'criteria']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['measuring'].label = 'Measuring Indicator (s)'
		self.fields['criteria'].label = 'Criteria for Overcoming'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('goals', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('measuring', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('criteria', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class PlanningDateForm(forms.ModelForm):
	ind_date = forms.DateField(label='Professional Behavior Date', widget=DateInput())
	class Meta:
		model = EvalPlanning
		fields = ['ind_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['ind_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('ind_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanningDate2Form(forms.ModelForm):
	obj_date = forms.DateField(label='Individual Objective Date', widget=DateInput())
	class Meta:
		model = EvalPlanning
		fields = ['obj_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['obj_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obj_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class PlanningEvaluatorDateForm(forms.ModelForm):
	eval_date_ind = forms.DateField(label='Professional Behavior Date', widget=DateInput())
	class Meta:
		model = EvalPlanning
		fields = ['eval_date_ind']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['eval_date_ind'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('eval_date_ind', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanningEvaluatorDate2Form(forms.ModelForm):
	eval_date_obj = forms.DateField(label='Individual Objective Date', widget=DateInput())
	class Meta:
		model = EvalPlanning
		fields = ['eval_date_obj']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['eval_date_obj'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('eval_date_obj', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanningIndividualForm(forms.ModelForm):
	progress = forms.CharField(label="Progress", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	dificulties = forms.CharField(label="Dificulties", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	need_improv = forms.CharField(label="Need Improvement", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalPlanningA
		fields = ['progress','dificulties', 'need_improv']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('progress', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('dificulties', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('need_improv', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class PlanningBehaviorForm(forms.ModelForm):
	progress = forms.CharField(label="Progress", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	dificulties = forms.CharField(label="Dificulties", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	need_improv = forms.CharField(label="Criteria for overcoming", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalPlanningB
		fields = ['progress','dificulties', 'need_improv']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('progress', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('dificulties', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('need_improv', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PlanningObjectiveForm(forms.ModelForm):
	objective = forms.CharField(label="Objectives", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalPlanningA
		fields = ['objective']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['objective'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('objective', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


# PRE - ASS
class PreAssIndividuoForm(forms.ModelForm):
	class Meta:
		model = EvalPreAssessmentA
		fields = ['scored']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('scored', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PreAssEvaluatorDateForm(forms.ModelForm):
	eval_ind_date = forms.DateField(label='Individual Objective Date', widget=DateInput())
	class Meta:
		model = EvalPreAssessment
		fields = ['eval_ind_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['eval_ind_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('eval_ind_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PreAssEvaluatorDate2Form(forms.ModelForm):
	eval_beh_date = forms.DateField(label='Professional Behavior Date', widget=DateInput())
	class Meta:
		model = EvalPreAssessment
		fields = ['eval_beh_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['eval_beh_date'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('eval_beh_date', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PreAssEvaluatorCommentForm(forms.ModelForm):
	comments = forms.CharField(label="Comments", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = EvalPreAssessment
		fields = ['comments']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['comments'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comments', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PreAssBehaviorForm(forms.ModelForm):
	class Meta:
		model = EvalPreAssessmentB
		fields = ['scored']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('scored', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
