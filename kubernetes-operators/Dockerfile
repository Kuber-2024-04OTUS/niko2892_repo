FROM python:3.8-slim
WORKDIR /app
ADD /kopf/ /app/kopf/
COPY requirements.txt /app
COPY mysql-operator.py /app
RUN pip install -r requirements.txt
CMD ["kopf","run","/app/mysql-operator.py"]