FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app/
RUN apk --no-cache add gcc musl-dev
RUN pip install -r requirements.txt
COPY . /app/
ENTRYPOINT ["python", "main.py", "--port=8080"]

