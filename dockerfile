FROM python:3.9.1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "./code/main.py", curl -X GET "localhost:9200/posts/_mapping?pretty"]
