FROM python:3.12.7
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
RUN pip install fastapi uvicorn

COPY . .

RUN chmod -R 777 /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]