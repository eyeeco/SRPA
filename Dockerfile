FROM python:3.5
MAINTAINER youchen <youchen.du@gmail.com>

RUN apt-get install -y git
RUN git clone https://github.com/Time1ess/SRPA
RUN pip install -r SRPA/requirements.txt

EXPOSE 8000

ENV SRPA_SETTINGS production

CMD ["/SRPA/scripts/server/start.sh"]
