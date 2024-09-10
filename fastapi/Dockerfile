FROM --platform=linux/arm64 python:3.12.6

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload"]