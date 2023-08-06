from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(TrainingPlan)
admin.site.register(TrainingEmp)
admin.site.register(ScholarshipPlan)
admin.site.register(ScholarshipEmp)
admin.site.register(ScholarshipEmpProgress)
admin.site.register(SType)
admin.site.register(SProgress)
admin.site.register(TrainingGap)
admin.site.register(TrainingDep)
admin.site.register(TrainingPlanGap)


@admin.register(TYear)
class TYearAdmin(ImportExportModelAdmin):
	pass
@admin.register(TType)
class TTypeAdmin(ImportExportModelAdmin):
	pass
@admin.register(TCriteria)
class TCriteriaAdmin(ImportExportModelAdmin):
	pass
@admin.register(TrainingCriteria)
class TrainingCriteriaAdmin(ImportExportModelAdmin):
	pass
