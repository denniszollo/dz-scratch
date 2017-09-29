echo $2
scp -o StrictHostKeyChecking=no $1 root@$2:/fw.bin

ssh -o StrictHostKeyChecking=no root@$2 'upgrade_tool --debug /fw.bin' > dev1.txt &

Sleep 100
echo Device 1 ouptut is $DEV1 `cat dev1.txt`

