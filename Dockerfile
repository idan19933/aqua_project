# Start from a lightweight Python base image
FROM python:3.10


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000


CMD ["python", "main.py"]
