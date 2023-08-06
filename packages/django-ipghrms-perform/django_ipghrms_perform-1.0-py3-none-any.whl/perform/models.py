from django.db import models
from django.contrib.auth.models import User
from contract.models import Category
from custom.models import Department, Position, Unit
from employee.models import Employee

class EvalMonth(models.Model):
	month = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self):
		template = '{0.month}'
		return template.format(self)
	
class EvalYear(models.Model):
	year = models.IntegerField(null=True, blank=True)
	is_active = models.BooleanField(default=False, null=True)
	def __str__(self):
		template = '{0.year} : {0.is_active}'
		return template.format(self)

class EvalType(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class EvalChoice(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	score = models.IntegerField(null=True, blank=True)
	def __str__(self):
		template = '{0.name}: {0.score}'
		return template.format(self)
	
class EvalChoicePlanning(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	score = models.IntegerField(null=True, blank=True)
	def __str__(self):
		template = '{0.name}: {0.score}'
		return template.format(self)
#
class ParameterA(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	measure = models.TextField(null=True, blank=True)
	criteria = models.TextField(null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class ParameterB(models.Model):
	area = models.CharField(max_length=100, null=True, blank=True)
	indicator = models.TextField(null=True, blank=True)
	def __str__(self):
		template = '{0.area}'
		return template.format(self)

# EVAL PLANNING
class EvalPlanning(models.Model):
	month = models.CharField(max_length=100, null=True, blank=True)
	year = models.ForeignKey(EvalYear, on_delete=models.CASCADE, null=True, blank=True, related_name="planningeval")
	type = models.ForeignKey(EvalType, on_delete=models.CASCADE, null=True, blank=True, related_name="planningeval")
	employeeeval = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="planningempeval")
	positioneval = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="planningempeval")
	uniteval = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='planningempeval')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="planningemp")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='planningemp')
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name='planningemp')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='planningeval')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='planningemp')
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	eval_date_obj = models.DateField(null=True, blank=True)
	eval_date_ind = models.DateField(null=True, blank=True)
	obj_date = models.DateField(null=True, blank=True)
	ind_date = models.DateField(null=True, blank=True)
	objective = models.TextField(null=True, blank=True, verbose_name="Objectives")
	is_lock = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.employee} - {0.year.year}'
		return template.format(self)

class EvalPlanningA(models.Model):
	eval = models.ForeignKey(EvalPlanning, on_delete=models.CASCADE, null=True, blank=True, related_name="evalplanninga")
	goals = models.TextField(null=True, blank=True, verbose_name="Goas/Activities")
	measuring = models.TextField(null=True, blank=True, verbose_name="Measuring Indicator")
	criteria = models.TextField(null=True, blank=True, verbose_name="Criteria for Overcoming")
	score = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	progress = models.TextField(null=True, blank=True, verbose_name="Progress")
	dificulties = models.TextField(null=True, blank=True, verbose_name="Dificulties")
	need_improv = models.TextField(null=True, blank=True, verbose_name="Need Improvement")
	enter_date = models.DateField(null=True, blank=True)
	eval_date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	usereval = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="evalplanningauser")
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.eval} - {0.eval.employee}'
		return template.format(self)
	

class EvalPlanningB(models.Model):
	eval = models.ForeignKey(EvalPlanning, on_delete=models.CASCADE, null=True, blank=True, related_name="evalplanningb")
	parameter = models.ForeignKey(ParameterB, on_delete=models.CASCADE, null=True, blank=True, related_name="evalplanningb")
	progress = models.TextField(null=True, blank=True)
	dificulties = models.TextField(null=True, blank=True)
	need_improv = models.TextField(null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	enter_date = models.DateField(null=True, blank=True)
	eval_date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	usereval = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="evalplanningbauser")
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.eval} - {0.eval.employee}'
		return template.format(self)
## END EVAL PLANNING
	

##EVAL
class Eval(models.Model):
	year = models.ForeignKey(EvalYear, on_delete=models.CASCADE, null=True, blank=True, related_name="eval")
	type = models.ForeignKey(EvalType, on_delete=models.CASCADE, null=True, blank=True, related_name="eval")
	employeeeval = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="evalevaluator")
	positioneval = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="evalevaluator")
	uniteval = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='evalevaluator')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="eval")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='eval')
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name='eval')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='eval')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='eval')
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	emp_obj_date = models.DateField(null=True, blank=True)
	emp_beh_date = models.DateField(null=True, blank=True)
	empeval_obj_date = models.DateField(null=True, blank=True)
	empeval_beh_date = models.DateField(null=True, blank=True)
	score_a = models.IntegerField(null=True, blank=True)
	score_b = models.IntegerField(null=True, blank=True)
	total = models.IntegerField(null=True, blank=True)
	outstanding_perf = models.TextField(null=True, blank=True, verbose_name="Justification Of Outstanding Performance")
	unsatisfactory_perf_obj = models.TextField(null=True, blank=True, verbose_name="Justification Of Unsatisfactory Performance - Individual Objectives")
	unsatisfactory_perf_beh = models.TextField(null=True, blank=True, verbose_name="Justification Of Unsatisfactory Performance - Professional Behaviors")
	recognition_merit = models.TextField(null=True, blank=True, verbose_name="Recognition of Merit (Outstanding Performance)")
	just_non_evaluation = models.TextField(null=True, blank=True, verbose_name="Jusitification of Non-Evaluation")
	comment_next_evaluation = models.TextField(null=True, blank=True, verbose_name="Expectations, Conditions And / Or Requirements for Personal And Professional Development")
	is_lock = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.employee} - {0.end_date}'
		return template.format(self)


class Evaluator(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="evaluator")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="evaluator")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="evaluator")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluator')
	def __str__(self):
		template = '{0.employee} - {0.position}'
		return template.format(self)

class EvalDate(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldate")
	date_a_1 = models.DateField(null=True, blank=True)
	date_a_2 = models.DateField(null=True, blank=True)
	date_b_1 = models.DateField(null=True, blank=True)
	date_b_2 = models.DateField(null=True, blank=True)
	def __str__(self):
		template = '{0.eval} - {0.date_a_1}'
		return template.format(self)

class EvalFinalScore(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="evalfinalscore")
	a = models.IntegerField(null=True, blank=True)
	b = models.IntegerField(null=True, blank=True)
	c = models.IntegerField(null=True, blank=True)
	d = models.IntegerField(null=True, blank=True)
	e = models.IntegerField(null=True, blank=True)
	def __str__(self):
		template = '{0.eval}: {0.a}/{0.b}/{0.c}/{0.d}/{0.e}'
		return template.format(self)
#
class EvalDetA(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldeta")
	parameter = models.ForeignKey(EvalPlanningA, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldeta")
	choice = models.ForeignKey(EvalChoice, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldeta")
	comments = models.TextField(null=True, blank=True, verbose_name="Komentariu")
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.parameter}: {0.choice}'
		return template.format(self)

class EvalDetB(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldetb")
	parameter = models.ForeignKey(EvalPlanningB, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldetb")
	choice = models.ForeignKey(EvalChoice, on_delete=models.CASCADE, null=True, blank=True, related_name="evaldetb")
	comments = models.TextField(null=True, blank=True, verbose_name="Komentariu")
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.parameter}: {0.choice}'
		return template.format(self)
	
# SELF ASSESSMENT
class EvalSelf(models.Model):
	year = models.ForeignKey(EvalYear, on_delete=models.CASCADE, null=True, blank=True, related_name="evalself")
	type = models.ForeignKey(EvalType, on_delete=models.CASCADE, null=True, blank=True, related_name="evalself")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="evalself")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='evalself')
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name='evalself')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='evalself')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='evalself')
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	ind_date = models.DateField(null=True, blank=True)
	beh_date = models.DateField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)
	is_lock = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.employee} - {0.end_date}'
		return template.format(self)

class EvalSelfDetA(models.Model):
	eval = models.ForeignKey(EvalSelf, on_delete=models.CASCADE, null=True, blank=True, related_name="evalselfdeta")
	parameter = models.ForeignKey(EvalPlanningA, on_delete=models.CASCADE, null=True, blank=True, related_name="evalselfdeta")
	comments_a = models.TextField(null=True, blank=True, verbose_name="Goal Exceeded")
	comments_b = models.TextField(null=True, blank=True, verbose_name="Goal Achieved")
	comments_c = models.TextField(null=True, blank=True, verbose_name="Goal Not Reached")
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.parameter}'
		return template.format(self)

class EvalSelfDetB(models.Model):
	eval = models.ForeignKey(EvalSelf, on_delete=models.CASCADE, null=True, blank=True, related_name="evalselfdetb")
	parameter = models.ForeignKey(EvalPlanningB, on_delete=models.CASCADE, null=True, blank=True, related_name="evalselfdetb")
	comments_a = models.TextField(null=True, blank=True)
	comments_b = models.TextField(null=True, blank=True)
	comments_c = models.TextField(null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.parameter}'
		return template.format(self)




# EVAL PRE - ASSESS
class EvalPreAssessment(models.Model):
	year = models.ForeignKey(EvalYear, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreass")
	type = models.ForeignKey(EvalType, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreass")
	employeeeval = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassempeval")
	positioneval = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassempeval")
	uniteval = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='evalpreassempeval')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassemp")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='evalpreassemp')
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name='evalpreassemp')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='evalpreass')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='evalpreassemp')
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	eval_ind_date = models.DateField(null=True, blank=True)
	eval_beh_date = models.DateField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)
	objective = models.TextField(null=True, blank=True, verbose_name="Objectives")
	is_lock = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.employee} - {0.end_date}'
		return template.format(self)
	

class EvalPreAssessmentA(models.Model):
	PRE_ASS_CHOICE_A = [
        ('one', 'Goal Exceeded (Explain)'),
        ('two', 'Goal Achived (Explain)'),
        ('three', 'Goal not Reached (Explain)'),
    ]
	eval = models.ForeignKey(EvalPreAssessment, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassa")
	plan_objective = models.ForeignKey(EvalPlanningA, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassaobjective")
	scored = models.CharField(max_length=100, choices=PRE_ASS_CHOICE_A, null=True, blank=True)
	enter_date = models.DateField(null=True, blank=True)
	eval_date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	usereval = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassauser")
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.eval} - {0.eval.employee}'
		return template.format(self)
	

class EvalPreAssessmentB(models.Model):
	PRE_ASS_CHOICE_B = [
        ('one', 'Demonstrated Competence at a High Level'),
        ('two', 'Goal Achived'),
        ('three', 'Goal not Reached'),
    ]
	eval = models.ForeignKey(EvalPreAssessment, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassb")
	parameter = models.ForeignKey(EvalPlanningB, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassbobjective")
	scored = models.CharField(max_length=100, choices=PRE_ASS_CHOICE_B, null=True, blank=True)
	enter_date = models.DateField(null=True, blank=True)
	eval_date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	usereval = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="evalpreassbuser")
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.eval} - {0.eval.employee}'
		return template.format(self)


