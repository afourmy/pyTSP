FROM python:3.6

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY gunicorn_config.py .

COPY source /source

EXPOSE 5000

CMD ["gunicorn", "--chdir", "source", "--config", "./gunicorn_config.py", "flask_app:app"]
