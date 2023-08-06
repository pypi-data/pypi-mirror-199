
from employee.models import Employee

def c_staff(user):
	employee = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser').first()
	return employee

def c_unit(user):
	employee = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','curempdivision','curempposition').first()
	return employee, employee.curempdivision.unit

def c_dep(user):
	employee = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','curempdivision','curempposition').first()
	return employee, employee.curempdivision.department

def c_user_deputy(user):
	employee = Employee.objects.filter(employeeuser__user=user, curempposition__position__code="Adjuntu")\
		.prefetch_related('employeeuser','curempposition').first()
	return employee

def c_user_de(user):
	employee = Employee.objects.filter(employeeuser__user=user, curempposition__position__code="DE")\
		.prefetch_related('employeeuser','curempposition').first()
	return employee
