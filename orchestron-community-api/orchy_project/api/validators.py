from django.core.files.uploadedfile import InMemoryUploadedFile,TemporaryUploadedFile
from rest_framework import serializers
from api.messages import *
from datetime import datetime
import os
from django.conf import settings

def empty_validator(data):
	if not data:
		raise serializers.ValidationError('This field may not be blank.')			

def file_only_validator(data):
	if not isinstance(data,InMemoryUploadedFile):
		raise serializers.ValidationError(FILE_VALIDATION)


def file_size_validator(data):
	max_size = 1024 * 1024 * settings.FILE_SIZE_LIMIT 
	if data.size > max_size:
		raise serializers.ValidationError(FILE_SIZE_VALIDATION.format(settings.FILE_SIZE_LIMIT))
	

def text_file_validator(data):
	if data:
		file_only_validator(data)
		file_size_validator(data)
		name,ext = os.path.splitext(data.name)
		content_type = data.content_type
		if ext != '.txt' or content_type not in ['text/plain']:
			raise serializers.ValidationError(TEXT_FILE_VALIDATION)					
	return data


def image_file_validator(data):
	if data:
		file_only_validator(data)
		file_size_validator(data)
		name,ext = os.path.splitext(data.name)
		content_type = data.content_type
		if ext not in ['.png','.jpg','.jpeg','.bmp','.gif','.tiff'] or content_type not in ['image/jpeg','image/png','image/bmp','image/gif','image/tiff']:
			raise serializers.ValidationError(IMAGE_FILE_VALIDATION)					
	return data


def flat_file_validator(data):
	if data:
		file_only_validator(data)
		file_size_validator(data)
		name,ext = os.path.splitext(data.name)
		content_type = data.content_type
		if ext not in ['.xml','.json']:
			raise serializers.ValidationError(FLAT_FILE_VALIDATION)					
	return data	


def start_date_validator(data):
	empty_validator(data)
	if data < datetime.today().date():			
		raise serializers.ValidationError(START_DATE_VALIDATION)
	return data


def end_date_validator(data):
	empty_validator(data)
	if data < datetime.today().date():			
		raise serializers.ValidationError(END_DATE_VALIDATION)
	return data		