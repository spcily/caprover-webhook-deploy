FROM python:3.8-slim-buster
RUN pip install requests
COPY deploy.py /deploy.py

ENTRYPOINT ["python3","/deploy.py"]
