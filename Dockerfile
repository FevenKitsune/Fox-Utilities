FROM python:3

WORKDIR /usr/src/app

RUN git clone https://github.com/FevenKitsune/Fox-Utilities.git
WORKDIR /usr/src/app/Fox-Utilities

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]