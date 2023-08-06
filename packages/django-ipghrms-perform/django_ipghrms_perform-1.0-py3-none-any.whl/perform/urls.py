from django.urls import path
from . import views

urlpatterns = [
	###
	path('c/dash/', views.cPerformDash, name="c-eval-dash"),
	path('c/list/', views.cPerformList, name="c-eval-list"),
	path('c/year/list/<str:year>/', views.cPerformYearList, name="c-eval-year-list"),
	path('c/cat/list/<str:pk>/', views.cPerformCatList, name="c-eval-cat-list"),
    
	##NEW
	path('conf/add-eval/<str:hashid>/<int:year>/', views.PerfomConfAddEval, name="eval-add-eval"),
	path('conf/detail-eval/<str:hashid>/<str:hashid2>/', views.PerfomEvalDetail, name="eval-detail-eval"),
	## EVAL EVALUATOR
    path('evaluator/add/<str:hashid>/<str:hashid2>/', views.PerfomEvalEvaluatorAdd, name="eval-evaluator-add"),
    path('evaluator/detail/<str:hashid>/<str:hashid2>/', views.PerfomEvalEvaluatorDetail, name="eval-evaluator-detail"),
	path('evaluator/updateA/<str:pk>/<str:hashid>/', views.PerformDetAUpdate, name="c-eval-update_a"),
	path('evaluator/updateB/<str:pk>/<str:hashid>/', views.PerformDetBUpdate, name="c-eval-update_b"),
	path('evaluator/lock/<str:hashid>/<str:hashid2>/', views.cPerformLock, name="c-eval-lock"),
	path('evaluator/refresh/<str:hashid>/<str:hashid2>/', views.cPerformRefresh, name="c-eval-refresh"),
	path('evaluator/update/outstanding/<str:hashid>/<int:pk>/', views.PerformEval4Update, name="c-eval-update-outstanding"),
	path('evaluator/update/unsatisfactory/A/<str:hashid>/<int:pk>/', views.PerformEval5Update, name="c-eval-update-uns-A"),
	path('evaluator/update/unsatisfactory/B/<str:hashid>/<int:pk>/', views.PerformEval6Update, name="c-eval-update-uns-B"),
	path('evaluator/update/merit/<str:hashid>/<int:pk>/', views.PerformEval7Update, name="c-eval-update-merit"),
	path('evaluator/update/jus-non-evaluation/<str:hashid>/<int:pk>/', views.PerformEval8Update, name="c-eval-update-jus-non-eval"),
	path('evaluator/update/expectation/<str:hashid>/<int:pk>/', views.PerformEval9Update, name="c-eval-update-exp"),
    

	path('c/add/', views.cPerformAdd, name="c-eval-add"),
	path('c/update/<str:hashid>/', views.cPerformUpdate, name="c-eval-update"),
	path('c/detail/<str:hashid>/', views.cPerformDetail, name="c-eval-detail"),
	path('c/remove/<str:hashid>/', views.cPerformRemove, name="c-eval-remove"),
	path('c/unlock/<str:hashid>/', views.cPerformUnlock, name="c-eval-unlock"),
	path('c/finish/<str:hashid>/', views.cPerformFinish, name="c-eval-finish"),
	path('c/date/update1/<str:pk>/', views.cPerformDate1Update, name="c-evaldate-update1"),
	path('c/date/update2/<str:pk>/', views.cPerformDate2Update, name="c-evaldate-update2"),
	#
	path('c/det/importA/<str:hashid>/', views.PerformDetAImport, name="c-eval-import_a"),
	path('c/det/importB/<str:hashid>/', views.PerformDetBImport, name="c-eval-import_b"),
	### ALL
	path('all/dash/', views.allPerformDash, name="all-eval-dash"),
	path('all/list/', views.allPerformList, name="all-eval-list"),
	path('all/detail/<str:hashid>/', views.allPerformDetail, name="all-eval-detail"),
	path('all/year/list/<str:year>/', views.allPerformYearList, name="all-eval-year-list"),
	path('all/cat/list/<str:pk>/', views.allPerformCatList, name="all-eval-cat-list"),
	path('all/cat/eval/list/<str:pk>/', views.allPerformCatEvalList, name="all-eval-cat-eval-list"),
	path('all/cat/not/list/<str:pk>/', views.allPerformCatNotList, name="all-eval-cat-not-list"),
	### CONF
	path('conf/dash/', views.PerformConfDash, name="eval-conf-dash"),
	path('conf/behavior/list/', views.PerformConfBehaviorList, name="eval-conf-behavior-list"),
	path('conf/year/active/<str:pk>/', views.PerformYearActive, name="eval-conf-year-active"),
	path('conf/eval/parama/add/', views.ParameterAAdd, name="eval-parama-add"),
	path('conf/eval/parama/update/<str:pk>/', views.ParameterAUpdate, name="eval-parama-update"),
	path('conf/eval/paramb/add/', views.ParameterBAdd, name="eval-paramb-add"),
	path('conf/eval/paramb/update/<str:pk>/', views.ParameterBUpdate, name="eval-paramb-update"),
	### PLAN
	path('conf/add/plan/<str:hashid>/<int:year>/', views.PerfomConfAddPlan, name="eval-conf-add-plan"),
	path('conf/add/plan-all/<int:year>/', views.PerfomConfAddPlanAll, name="eval-conf-add-plan-all"),
	path('conf/plan-detail/<str:hashid>/', views.PerfomPlanDetail, name="eval-conf-plan-detail"),
	path('conf/plan-add/A/<str:hashid>/', views.PerfomPlanAddA, name="eval-conf-plan-add-a"),
	path('conf/plan-update/A/<str:hashid>/', views.PerfomPlanUdpateA, name="eval-conf-plan-update-a"),
	path('conf/plan-delete/A/<str:hashid>/<str:hashid2>/', views.PerfomPlanDeleteA, name="eval-conf-plan-delete-a"),
	path('conf/behavior-add/B/<str:hashid>/', views.PerformConfBehaviorAdd, name="eval-conf-plan-add-b"),
	path('conf/behavior-delete/B/<str:hashid>/<str:hashid2>/', views.PerfomPlanDeleteB, name="eval-conf-behavior-delete-b"),
	path('conf/plan-add/objective/<str:hashid>/', views.PerfomPlanAddObjective, name="eval-conf-plan-add-objectives"),
	path('conf/plan-lock/<str:hashid>/', views.PerfomPlanLock, name="eval-conf-plan-lock"),
	path('conf/plan-add/beh-date/<str:hashid>/', views.PerfomPlanAddBehDate, name="eval-conf-plan-add-beh-date"),
	path('conf/plan-add/obj-date/<str:hashid>/', views.PerfomPlanAddObjDate, name="eval-conf-plan-add-obj-date"),


	## PLAN EVALUATOR
	path('plan-evaluator/add/<str:hashid>/', views.PerfomPlanEvaluatorAdd, name="eval-conf-plan-evaluator-add"),
	path('plan-evaluator/detail/<str:hashid>/', views.PerfomPlanEvaluatorDetail, name="eval-conf-plan-evaluator-detail"),
	path('plan-evaluator/individual/add/<str:hashid>/', views.PerfomPlanIndividualAdd, name="eval-conf-plan-evaluator-ind-add"),
	path('plan-evaluator/behavior/add/<str:hashid>/', views.PerfomPlanBehaviorAdd, name="eval-conf-plan-evaluator-beh-add"),
	path('plan-evaluator/lock/<str:hashid>/', views.PerfomPlanEvaluatorLock, name="eval-conf-plan-evaluator-lock"),
	path('plan-eval-add/beh-date/<str:hashid>/', views.PerfomPlanEvalAddBehDate, name="eval-conf-plan-eval-add-beh-date"),
	path('plan-eval-add/obj-date/<str:hashid>/', views.PerfomPlanEvalAddObjDate, name="eval-conf-plan-eval-add-obj-date"),
	 
	###PRE ASSESSMENT ###
	path('conf/add/pre-ass/<str:hashid>/<int:year>/', views.PerfomConfAddPreAss, name="eval-conf-add-pre-ass"),
	path('conf/pre-ass/detail/<str:hashid>/', views.PerfomConfPreAssDetail, name="eval-conf-pre-ass-detail"),
	path('conf/pre-ass-lock/<str:hashid>/', views.PerfomPreAssLock, name="eval-pre-ass-lock"),
	path('conf/add/A/pre-ass/<str:hashid>/', views.PerfomConfPreAssAddA, name="eval-conf-pre-ass-add-a"),
	path('conf/add/B/pre-ass/<str:hashid>/', views.PerfomConfPreAssAddB, name="eval-conf-pre-ass-add-b"),
	path('preass-evaluator/add/<str:hashid>/', views.PerfomEvaluatorAdd, name="eval-pre-ass-evaluator-add"),
	path('preass-evaluator/detail/<str:hashid>/', views.PerfomEvaluatorDetail, name="eval-pre-ass-evaluator-detail"),
	path('preass-evaluator/add-ind/<str:hashid>/', views.PerfomEvaluatorIndAdd, name="eval-pre-ass-evaluator-add-ind"),
	path('preass-evaluator/add-beh/<str:hashid>/', views.PerfomEvaluatorBehAdd, name="eval-pre-ass-evaluator-add-beh"),
	path('preass-evaluator/lock/<str:hashid>/', views.PerfomEvaluatorLock, name="eval-pre-ass-evaluator-lock"),
	path('preass-evaluator/add-date1/<str:hashid>/', views.PerfomPreAssEvalAddObjDate, name="eval-pre-ass-evaluator-add-date-obj"),
	path('preass-evaluator/add-date2/<str:hashid>/', views.PerfomPreAssEvalAddBehDate, name="eval-pre-ass-evaluator-add-date-beh"),
	path('preass-evaluator/add-comment/<str:hashid>/', views.PerfomPreAssEvalAddComment, name="eval-pre-ass-evaluator-add-comment"),
	

	### SELF
	path('self/add/<str:hashid>/<int:year>/', views.PerfomConfAddSelfEval, name="hr-eval-self-add"),
	path('self/conf-detail/<str:hashid>/', views.PerfomConfSelfDetail, name="hr-eval-self-detail"),
	path('self/add-ind/<str:hashid>/', views.selfPerformDetAUpdate, name="eval-self-add-ind"),
	path('self/add-bhv/<str:hashid>/', views.selfPerformDetBUpdate, name="eval-self-add-bhv"),
	path('self/lock/<str:hashid>/', views.selfPerformLock, name="eval-self-lock"),
	path('self/add-date1/<str:hashid>/', views.SelfEvalAddObjDate, name="eval-self-add-date-obj"),
	path('self/add-date2/<str:hashid>/', views.SelfEvalAddBehDate, name="eval-self-add-date-beh"),
	path('self/add-comment/<str:hashid>/', views.SelfEvalAddComment, name="eval-self-add-comment"),
    
	##EVALUATOR SELF
	path('evaluator-self/detail/<str:hashid>/', views.PerfomEvaluatorSelfDetail, name="evaluator-eval-self-detail"),

    path('self/list/', views.selfPerformList, name="eval-self-list"),
	path('self/add/<str:page>/', views.selfPerformAdd, name="eval-self-add"),
	path('self/detail/<str:hashid>/', views.selfPerformDetail, name="eval-self-detail"),
	path('self/update/<str:hashid>/', views.selfPerformUpdate, name="eval-self-update"),
	path('self/com/update/<str:hashid>/', views.selfPerformComUpdate, name="eval-self-com-update"),
	path('self/remove/<str:hashid>/', views.selfPerformRemove, name="eval-self-remove"),
	path('self/unlock/<str:hashid>/', views.selfPerformUnlock, name="eval-self-unlock"),
	path('self/finish/<str:hashid>/', views.selfPerformFinish, name="eval-self-finish"),

	path('emp/s/det/importA/<str:hashid>/', views.selfPerformDetAImport, name="eval-self-import_a"),
	path('emp/s/det/updateA/<str:pk>/<str:hashid>/', views.selfPerformDetAUpdate, name="eval-self-update_a"),
	path('emp/s/det/importB/<str:hashid>/', views.selfPerformDetBImport, name="eval-self-import_b"),
	# path('emp/s/det/updateB/<str:pk>/<str:hashid>/', views.selfPerformDetBUpdate, name="eval-self-update_b"),
	#
	path('self/all/list/', views.selfPerformAllList, name="eval-self-all-list"),
	path('self/year/list/<str:year>/', views.selfPerformYearList, name="eval-self-year-list"),
	path('self/unit/list/', views.selfPerformUnitList, name="eval-self-unit-list"),
	path('self/unit/year/list/<str:year>/', views.selfPerformUnitYearList, name="eval-self-unit-year-list"),
	path('self/all/detail/<str:hashid>/', views.selfPerformAllDetail, name="eval-self-all-detail"),
    
	### STAFF
	path('staff/list/', views.StaffListPerfom, name="staff-perform-list"),
    
	### STAFF PLAN
	path('staff/plan-detail/<str:hashid>/', views.StaffPerfomPlanDetail, name="staff-perform-plan-detail"),
    
	### STAFF PRE ASS
	path('staff/preass-detail/<str:hashid>/', views.StaffPerfomPreAssDetail, name="staff-perform-preass-detail"),
	### SELF
	path('staff/self-detail/<str:hashid>/', views.StaffPerformSelfDetail, name="staff-perform-self-detail"),
    ### EVAL
    path('staff/eval-detail/<str:hashid>/<str:hashid2>/', views.StaffEvalDetail, name="staff-eval-detail"),
]