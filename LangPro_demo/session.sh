#!/bin/bash

tmux new -d -s "foo" 'bash --init-file start.sh'
tmux set-environment -t "foo" PYTHONPATH "/git_LangPro/python:$PYTHONPATH"
tmux splitw -t "foo"
tmux a -t foo
