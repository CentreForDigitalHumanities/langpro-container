#!/bin/bash

bash fixes.sh
apachectl -k start
export PYTHONPATH="/git_LangPro/python:$PYTHONPATH"
python3 server.py
