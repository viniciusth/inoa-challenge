sleep 5s
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runworkers & 
python3 manage.py runserver 0.0.0.0:8000