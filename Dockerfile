FROM python:3.9.5-buster
WORKDIR /app
RUN chmod 777 /app
RUN pip3 install -U pip
RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6 -y
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["python3 -m spr", "runserver", "0.0.0.0:4000"]
