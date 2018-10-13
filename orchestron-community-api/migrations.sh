/usr/bin/python3 /webapps/orchestron_community_api/manage.py makemigrations api 
/usr/bin/python3 /webapps/orchestron_community_api/manage.py migrate
python3 /webapps/orchestron_community_api/manage.py shell -c "from api.models import User; User.objects.create_superuser('admin', '$1', '$2')" || true