FROM python:3.12-slim


RUN apt update && apt install -y ffmpeg


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "bot.py"]
