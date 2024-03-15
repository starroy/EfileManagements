FROM python:3.10-slim 


ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt /tmp/.

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt -y upgrade
RUN apt install -y python3-pip  \
libgl1 ffmpeg libsm6 libxext6 git pkg-config default-libmysqlclient-dev
COPY requirements.txt /tmp/requirements.txt

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# running migrations

# gunicorn

