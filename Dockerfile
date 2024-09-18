# syntax=docker/dockerfile:1
FROM python:3.11

WORKDIR /code
ENV DJANGO_DEBUG=0

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py makemigrations && python manage.py migrate

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
CMD ["sh", "start.sh"]