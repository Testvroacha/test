FROM python:3.9.5-buster
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN mkdir /app
WORKDIR /app
RUN chmod 777 /app
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -U -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python3", "-m", "spr", "runserver", "0.0.0.0:8000"]
