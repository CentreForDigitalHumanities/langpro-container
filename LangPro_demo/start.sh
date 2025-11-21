#!/bin/bash

bash fixes.sh
apachectl -k start
export PYTHONPATH="/git_LangPro/python:$PYTHONPATH"
sudo -u www-data:www-data python3 server.py
