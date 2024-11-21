FROM python:3.12.6

WORKDIR /usr/src/app
COPY ./ ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "api/main.py", "--port", "80"]