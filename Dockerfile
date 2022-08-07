FROM python:3.9.5-buster
WORKDIR /app
RUN chmod 777 /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .

CMD ["python3", "-m", "spr"]
