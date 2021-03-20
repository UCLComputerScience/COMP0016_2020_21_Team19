FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN chmod +x /code/start.sh
RUN chmod +x /code/init_db.sh

EXPOSE 8000

CMD ["/code/start.sh"]