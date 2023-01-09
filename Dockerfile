FROM python:3.9.16-slim

WORKDIR /Timelaps

copy . .

RUN apt-get update && apt-get install -y cron
#ffmpeg libgl1 libsm6 libxext6 libxrender-dev

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN pip install opencv-python-headless

RUN chmod 0644 crontab

#ENV PATH=/home/t_t/home_server:$PATH

RUN crontab crontab

CMD ["cron","-f", "-l", "2"] # running corn in the foregraound, beceause it runing in container 
#debian/ubuntu < cron -f -l 2 >  alpine < crond -f -l 2 > centos <crond -n>
