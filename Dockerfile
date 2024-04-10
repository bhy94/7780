FROM python:3.12-slim

WORKDIR /app

COPY ./backend /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV SERVICE_PORT 8080

CMD uvicorn main:app --host 0.0.0.0 --port $SERVICE_PORT
# CMD python test.py