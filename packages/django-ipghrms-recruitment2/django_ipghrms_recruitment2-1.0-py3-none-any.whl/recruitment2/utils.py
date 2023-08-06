import os
from uuid import uuid4

def upload_rec_prop(instance, filename):
	upload_to = 'recfiles/{}/'.format(instance.id)
	field = 'prop'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.id,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_rec_attach(instance, filename):
	upload_to = 'recfiles/{}/'.format(instance.id)
	field = 'attach'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_rec_written(instance, filename):
	upload_to = 'recfiles/{}/'.format(instance.id)
	field = 'written'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
	
def upload_rec_oral(instance, filename):
	upload_to = 'recfiles/{}/'.format(instance.id)
	field = 'oral'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_rec_tor(instance, filename):
	upload_to = 'recfiles/{}/'.format(instance.plan.id)
	field = 'tor'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.plan.id,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_can_cv(instance, filename):
	upload_to = 'recfiles/cand/{}/'.format(instance.id)
	field = 'cv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.id,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)


