FROM python:3.6

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./app/ ./
CMD ["celery","-A", "app.celeryapp", "worker", "--loglevel=info"]
