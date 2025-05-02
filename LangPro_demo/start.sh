#!/bin/bash

bash fixes.sh
apachectl -k start
python3 server.py
