#!/bin/bash
echo "index,pc_time"
cat $1 | jq -cr '. | [.time, .data.msg_type]' | sed 's/[]""[]//' 
