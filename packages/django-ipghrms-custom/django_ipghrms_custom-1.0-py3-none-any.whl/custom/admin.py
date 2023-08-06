from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


admin.site.register(DE)
admin.site.register(Unit)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(EducationLevel)
admin.site.register(Municipality)
admin.site.register(Language)
admin.site.register(Grade)
admin.site.register(Echelon)

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
	pass
@admin.register(Year)
class YearAdmin(ImportExportModelAdmin):
	pass
@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
	pass
@admin.register(FamilyRelation)
class FamilyRelationAdmin(ImportExportModelAdmin):
	pass
