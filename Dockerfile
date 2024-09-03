FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


COPY ./requirements.txt /requirements.txt
COPY . /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/pip install pip==21.3.1

RUN pip install -r /requirements.txt

WORKDIR /app

# RUN chmod +x ./startup.sh
# CMD ["/bin/sh", "-c", "./startup.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]

# uvicorn main:app --host 0.0.0.0 --port 80 --reload



# docker buildx build --platform=linux/amd64 -t

# docker build -t federerjiang/ocr-api-hf:v1.0 .

# docker run -d -p 80:80 ocr-api-hf

# docker buildx build --platform linux/amd64,linux/arm64 -t federerjiang/ocr-api-hf:v1.0 --push .