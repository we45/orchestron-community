from django.core.files.storage import FileSystemStorage
import json
from api.minio_utils import MinioUtil
from uuid import uuid4


class OverwriteStorage(FileSystemStorage):
	def _save(self, name, content):
		MinioUtil().upload_file(name, content)
		return super(OverwriteStorage, self)._save(name, content)

	def get_available_name(self, name, max_length):
		file_name = name.split('/')[-1]
		ext = file_name.split('.')[-1]
		uuid_name = '{0}.{1}'.format(str(uuid4()),ext)
		name = name.replace(file_name,uuid_name)
		return name