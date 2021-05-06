#!/usr/bin/bash
export HOME="/home/galaxy"
python /galaxy/tools/toolfactory/toolwatcher.py > /var/log/toolwatcher.log
