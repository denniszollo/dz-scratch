#!/bin/bash
f=$1
echo $f
pyt=$(cat <<EOF
import base64
import sys
for each in sys.stdin.readlines():
  print ":".join(base64.b64decode(each).split("\0")[1:])
EOF
)
cat $f | jq -cr '. | select(.data.msg_type == 167) | [.data.payload]'  | python -c "$pyt"
