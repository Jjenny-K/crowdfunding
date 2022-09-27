FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /crowdfunding
ADD . /crowdfunding
WORKDIR /crowdfunding

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN python3 manage.py migrate --settings=config.settings.deploy
RUN python3 manage.py collectstatic --settings=config.settings.deploy


EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi.deploy:application"]
