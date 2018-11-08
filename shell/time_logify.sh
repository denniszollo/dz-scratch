#!/bin/bash
echo "index,pc_time,elapsed_time,level,msg_log"
cat $1 | jq -cr '. | select(.data.msg_type == 1025) | [.time, .data.payload]' | sed 's/[]""[]//' > /tmp/out.csv
python ../python/time_log.py /tmp/out.csv
