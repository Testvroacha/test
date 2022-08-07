FROM python:3.9.5-buster
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
WORKDIR /app
RUN chmod 777 /app
COPY requirements.txt .
RUN pip3 install -U pip && pip3 install --no-cache-dir -U -r requirements.txt
COPY . .

EXPOSE 8000

RUN ["python3", "-m", "spr", "runserver", "0.0.0.0:8000"]
