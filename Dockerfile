FROM python:3.9-slim

WORKDIR /app

COPY exporter.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV EXPORTER_HOST=0.0.0.0
ENV EXPORTER_PORT=8080

CMD ["python", "exporter.py"]
