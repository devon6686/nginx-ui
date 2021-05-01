#!/bin/bash

if ps aux | grep -i uwsgi &> /dev/null;then
  pkill -9 uwsgi
  sleep 2
fi
/usr/local/bin/uwsgi --socket "0.0.0.0:8000" --wsgi-file wsgi.py --callable app --master --daemonize ./ui.log
