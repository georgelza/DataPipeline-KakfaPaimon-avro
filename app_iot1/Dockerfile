
FROM python:3.12-bookworm

USER root:root

WORKDIR /app
RUN mkdir logs
RUN mkdir conf

COPY requirements .
RUN pip install --upgrade pip
RUN pip install -r requirements

COPY *.py .

LABEL Author="George Leonard (georgelza@gmail.com)"

ENTRYPOINT [ "python3", "main.py" ]


