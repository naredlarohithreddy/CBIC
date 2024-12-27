# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12.8-slim

EXPOSE 8000

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "server:app"]