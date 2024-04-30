FROM python:3.10.11-alpine3.16

WORKDIR /srv/numedy_test_task/

COPY exec.sh ./exec.sh
COPY req.txt ./req.txt
ADD . .

RUN apk add --update build-base 

RUN chmod +x ./exec.sh

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install psycopg2-binary

RUN pip install -r ./req.txt 

ENTRYPOINT ["sh", "/srv/numedy_test_task/exec.sh"] 