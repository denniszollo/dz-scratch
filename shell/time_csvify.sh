#!/bin/bash
echo "index,pc_time,pc_time_dt,piksi_time,time_diff"
cat $1 | jq -cr '. | select(.data.msg_type == 259) | [.time, .data.payload]' | sed 's/[]"[]//g' > /tmp/out.csv
python ../python/convert_gps_time_json_to_csv.py /tmp/out.csv
