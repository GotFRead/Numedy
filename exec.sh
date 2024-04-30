#!bin/sh
cd /srv/numedy_test_task &&
alembic upgrade 72bacd508cc1 &&
python3 ./main.py
