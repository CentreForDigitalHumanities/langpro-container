#!/bin/bash

bash fixes.sh
apachectl -k start
export PYTHONPATH="/git_LangPro/python:$PYTHONPATH"
runuser -u www-data python3 server.py
