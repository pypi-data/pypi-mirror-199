import os
from uuid import uuid4

def upload_civilstatus(instance, filename):
	upload_to = 'employee_files/{}'.format(instance.id)
	field = 'civil_status'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_photo(instance, filename):
	upload_to = 'employee_files/{}'.format(instance.employee.id)
	field = 'photo'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.employee.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_signature(instance, filename):
	upload_to = 'employee_files/{}'.format(instance.employee.id)
	field = 'signature'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.employee.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_formal(instance, filename):
	upload_to = 'employee_files/{}/formal/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_nonformal(instance, filename):
	upload_to = 'employee_files/{}/nonformal/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_depend(instance, filename):
	upload_to = 'employee_files/{}/depend/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_attendace(instance, filename):
	upload_to = 'absensia/{}/{}'.format(instance.unit.id, instance.year)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.year,instance.month,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_trip(instance, filename):
	upload_to = 'trip/{}/{}'.format(instance.id, instance.date_out.year)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.date_out.year,instance.date_out.month,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_perform(instance, filename):
	upload_to = 'employee_files/{}/evaluation/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.year,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_contract(instance, filename):
	upload_to = 'employee_files/{}/contract/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
def upload_contract_end(instance, filename):
	upload_to = 'employee_files/{}/contract_end/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_position(instance, filename):
	upload_to = 'employee_files/{}/position/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_place(instance, filename):
	upload_to = 'employee_files/{}/place/'.format(instance.employee.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_languages(instance, filename):
	upload_to = 'languages/{}'.format(instance.employee.id)
	field = 'languages'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_leave(instance, filename):
	upload_to = 'leave/{}/'.format(instance.employee.id)
	field = 'leave'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_training(instance, filename):
	upload_to = 'training/'.format(instance.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_training_subject(instance, filename):
	upload_to = 'training/subject/'.format(instance.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.employee.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_scholarship(instance, filename):
	upload_to = 'scholarship/'.format(instance.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.start_date,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)


def upload_id_card(instance, filename):
	upload_to = 'employee_files/{}/idcards/'.format(instance.employee.id)
	ext = filename.split('.')[-1]
	filename = '{}_{}.{}'.format(uuid4().hex,instance.employee.id,ext)
	return os.path.join(upload_to, filename)

def upload_rec_tor(instance, filename):
	upload_to = 'recruitment/{}/'.format(instance.plan.id)
	field = 'tor'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.plan.id,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_logo(instance, filename):
	upload_to = 'logo/{}'.format(instance.id)
	field = 'ipg_logo'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cop(instance, filename):
	upload_to = 'cop/{}'.format(instance.id)
	field = 'ipg_cop'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_organograma(instance, filename):
	upload_to = 'organograma/{}/'.format(instance.id)
	field = 'organograma'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

