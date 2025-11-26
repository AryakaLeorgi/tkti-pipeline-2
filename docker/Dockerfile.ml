FROM python:3.10-slim

WORKDIR /app

# Install ML dependencies
COPY requirements-ml.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app

CMD ["python3", "src/ml/infer.py"]
