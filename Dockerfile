FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./protype/ /code/

# This is a bad idea, but it can be removed later. 
# Its a hack for dev mode only.
CMD ./manage.py migrate

ENTRYPOINT ["python",  "manage.py", "runserver", "0.0.0.0:8000"]