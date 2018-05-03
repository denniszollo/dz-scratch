FILES=$(ls serial-link-20180320-145340.log.json)
for f in $FILES
do
  echo $f
  filename="${f%.*}"
  VERSION=$(cat $f | jq -cr '. | select(.data.msg_type == 167) | [.data.setting]' | grep  'system_info\\u0000firmware_version\\u0000' | cut -c42- | cut -f1 -d '\')
  echo $VERSION
  #mkdir -p $VERSION
  #mv $filename* $VERSION/$f
done
