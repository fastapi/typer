FROM python:3.7

RUN pip install "pydantic==1.5.1" pygithub

COPY ./app /app

CMD ["python", "/app/main.py"]
