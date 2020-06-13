FROM python:3.6

COPY requirements.txt ./
RUN pip install -r requirements.txt
ADD ./app/ /app
WORKDIR /app
CMD ["python","app.py"]
