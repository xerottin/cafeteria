FROM python:3.11-slim

WORKDIR /app
RUN apt-get update --fix-missing && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


ADD . /app

EXPOSE 8009

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]