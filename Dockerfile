FROM python:3.9
WORKDIR /almuassa/app

RUN pip3 install --upgrade pip 
COPY requirements.txt .
RUN pip3 install -r requirements.txt 
COPY . .

# RUN python manage.py collectstatic --noinput
CMD uwsgi --http=0.0.0.0:80 --module=mouasah.wsgi
