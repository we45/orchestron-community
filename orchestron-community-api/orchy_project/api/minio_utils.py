from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists, NoSuchBucket, InvalidAccessKeyId, \
	SignatureDoesNotMatch, NoSuchKey
from django.conf import settings
from api.exceptions import MinioResponseError, MinioNoFileError

class MinioUtil:
	def __init__(self):
		self.bucket_name = settings.MINIO.get('bucket_name')
		self.connection = Minio(settings.MINIO.get('url'),
	                  access_key=settings.MINIO.get('access_key'),
	                  secret_key=settings.MINIO.get('secret_key'),
	                  secure=False)
		
	def create_bucket(self):
		try:
			self.connection.make_bucket(self.bucket_name)
		except (BucketAlreadyOwnedByYou, BucketAlreadyExists) as err:
			pass
		except ResponseError as err:
			raise MinioResponseError

	def upload_file(self, file_name, file_content):
		try:
			self.connection.put_object(self.bucket_name, file_name, file_content, length=file_content.size)
		except ResponseError as err:
			raise MinioResponseError
		except NoSuchBucket:
			self.create_bucket()
			raise MinioResponseError

	def upload_file_from_path(self, file_name, file_path):
		try:
			self.connection.fput_object(self.bucket_name, file_name, file_path)
		except ResponseError as err:
			raise MinioResponseError
		except NoSuchBucket:
			self.create_bucket()
			raise MinioResponseError			

	def get_file(self, file_name):
		try:
			return self.connection.get_object(self.bucket_name, file_name)
		except ResponseError as err:
			raise MinioResponseError
		except NoSuchKey:
			raise MinioNoFileError			


	

	