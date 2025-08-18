FROM python:3.13.7-slim

# don't buffer python output to stdout
ENV PYTHONUNBUFFERED=1
# suppress pip version warning
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY helper.py scheduler.py sync_grocy.py /app/

WORKDIR /app

VOLUME ["/app/data"]

CMD ["python", "/app/scheduler.py"]