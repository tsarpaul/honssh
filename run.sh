#!/bin/bash

python cleanupd.py &
rm ./honssh.pid; ./update.sh; ./honsshctrl.sh start

