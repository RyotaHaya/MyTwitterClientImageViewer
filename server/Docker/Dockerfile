FROM tiangolo/uvicorn-gunicorn:python3.9
WORKDIR /app

COPY ../../server /app/

RUN pip install  pipenv && \
    pip install fastapi uvicorn

RUN pipenv install

EXPOSE 80
CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "80"]