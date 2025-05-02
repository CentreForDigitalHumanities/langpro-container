#!/bin/bash

tmux new -d -s "foo" 'bash --init-file start.sh'
tmux splitw -t "foo"
tmux a -t foo
