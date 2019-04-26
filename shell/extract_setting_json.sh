f=$1
echo $f
VERSION=$(cat $f | jq -cr '. | select(.data.msg_type == 175) | [.data.payload]'  | python -m base64 -d) 
echo $VERSION
