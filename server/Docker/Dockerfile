FROM python:3.10.4-slim-bullseye

# Set environment variables.
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app
COPY ../../server /app/

RUN pip install  pipenv && \
    pip install fastapi uvicorn

RUN pipenv install

EXPOSE 80
CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "80"]