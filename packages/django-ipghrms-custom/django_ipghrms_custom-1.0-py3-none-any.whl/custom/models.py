from django.db import models

class DE(models.Model):
	code = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Unit(models.Model):
	leader = models.ForeignKey(DE, on_delete=models.CASCADE, null=True ,blank=True)
	code = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name} ({0.code})'
		return template.format(self)
	class Meta:
		verbose_name = "Divizaun"

class Department(models.Model):
	leader = models.ForeignKey(DE, on_delete=models.CASCADE, null=True,blank=True)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
	code = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name} ({0.code})'
		return template.format(self)

class Position(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=20, null=True, blank=True)
	def __str__(self):
		template = '{0.name}-{0.code}'
		return template.format(self)

class EducationLevel(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Country(models.Model):
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=50)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Municipality(models.Model):
	code = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=100)
	hckey = models.CharField(max_length=10, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Village(models.Model):
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Aldeia(models.Model):
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class University(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Year(models.Model):
	year = models.IntegerField(null=True, blank=True)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class Language(models.Model):
	name = models.CharField(max_length=100, verbose_name="Lingua")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class FamilyRelation(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
###
class Grade(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Echelon(models.Model):
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=10)
	def __str__(self):
		template = '{0.code}'
		return template.format(self)

class ADNInfo(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	def __str__(self):
		template = '{0.name}-{0.address}'
		return template.format(self)
